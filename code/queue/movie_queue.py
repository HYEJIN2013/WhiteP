import logging
from optparse import OptionValueError
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.exc import OperationalError
from flexget.manager import Session
from flexget.utils import qualities
from flexget.utils.imdb import extract_id, ImdbSearch, ImdbParser
from flexget.utils.database import quality_synonym
from flexget.utils.tools import console, str_to_boolean
from flexget.plugin import DependencyError, PluginError, get_plugin_by_name, register_plugin, register_parser_option
from flexget.schema import versioned_base

try:
    from flexget.plugins.filter import queue_base
except ImportError:
    raise DependencyError(issued_by='movie_queue', missing='queue_base',
                             message='movie_queue requires the queue_base plugin')

log = logging.getLogger('movie_queue')
Base = versioned_base('movie_queue', 0)


class QueuedMovie(queue_base.QueuedItem, Base):
    __tablename__ = 'movie_queue'
    __mapper_args__ = {'polymorphic_identity': 'movie'}
    id = Column(Integer, ForeignKey('queue.id'), primary_key=True)
    imdb_id = Column(String)
    tmdb_id = Column(Integer)
    _quality = Column('quality', String)
    quality = quality_synonym('_quality')


class FilterMovieQueue(queue_base.FilterQueueBase):

    def matches(self, feed, config, entry):
        # make sure the entry has IMDB fields filled
        try:
            get_plugin_by_name('imdb_lookup').instance.lookup(feed, entry)
        except PluginError:
            # no IMDB data, can't do anything
            return

        imdb_id = None
        if entry.get('imdb_id'):
            imdb_id = entry['imdb_id']
        elif entry.get('imdb_url'):
            imdb_id = extract_id(entry['imdb_url'])

        if not imdb_id:
            log.warning("No imdb id could be determined for %s" % entry['title'])
            return

        return feed.session.query(QueuedMovie).filter(QueuedMovie.imdb_id == imdb_id).\
                                               filter(QueuedMovie.downloaded == None).first()


class QueueError(Exception):
    """Exception raised if there is an error with a queue operation"""

    # TODO: I think message was removed from exception baseclass and is now masked
    # some other custom exception (DependencyError) had to make so tweaks to make it work ..

    def __init__(self, message, errno=0):
        self.message = message
        self.errno = errno


class MovieQueueManager(object):
    """
    Handle IMDb queue management; add, delete and list
    """


    options = {}

    @staticmethod
    def optik_imdb_queue(option, opt, value, parser):
        """
        Callback for Optik
        --imdb-queue (add|del|list) [IMDB_URL|NAME] [quality]
        """
        options = {}
        usage_error = OptionValueError('Usage: --movie-queue (add|del|list) [IMDB_URL|NAME] [QUALITY] [FORCE]')
        if not parser.rargs:
            raise usage_error

        options['action'] = parser.rargs[0].lower()
        if options['action'] not in ['add', 'del', 'list']:
            raise usage_error

        if len(parser.rargs) == 1:
            if options['action'] != 'list':
                raise usage_error

        # 2 args is the minimum allowed (operation + item) for actions other than list
        if len(parser.rargs) >= 2:
            options['what'] = parser.rargs[1]

        # 3, quality
        if len(parser.rargs) >= 3:
            options['quality'] = parser.rargs[2]
        else:
            options['quality'] = 'ANY' # TODO: Get default from config somehow?

        # 4, force download
        if len(parser.rargs) >= 4:
            options['force'] = str_to_boolean(parser.rargs[3])
        else:
            options['force'] = True

        parser.values.movie_queue = options

    def parse_what(self, what):
        """Given an imdb id or movie title, looks up from imdb and returns a dict with imdb_id and title keys"""
        imdb_id = extract_id(what)
        title = what

        if imdb_id:
            # Given an imdb id, find title
            parser = ImdbParser()
            try:
                parser.parse('http://www.imdb.com/title/%s' % imdb_id)
            except Exception:
                raise QueueError('Error parsing info from imdb for %s' % imdb_id)
            if parser.name:
                title = parser.name
        else:
            # Given a title, try to do imdb search for id
            console('Searching imdb for %s' % what)
            search = ImdbSearch()
            result = search.smart_match(what)
            if not result:
                raise QueueError('ERROR: Unable to find any such movie from imdb, use imdb url instead.')
            imdb_id = extract_id(result['url'])
            title = result['name']

        self.options['imdb_id'] = imdb_id
        self.options['title'] = title
        return {'title': title, 'imdb_id': imdb_id}

    def on_process_start(self, feed):
        """
        Handle IMDb queue management
        """

        if not getattr(feed.manager.options, 'movie_queue', False):
            return

        feed.manager.disable_feeds()

        options = feed.manager.options.movie_queue

        if options['action'] == 'list':
            self.queue_list()
            return

        # all actions except list require imdb_url to work
        # Generate imdb_id and movie title from movie name, or imdb_url
        try:
            what = self.parse_what(options['what'])
        except QueueError, e:
            console(e.message)
        else:
            options.update(what)

        if not options.get('title') or not options.get('imdb_id'):
            console('could not determine movie to add') # TODO: Rethink errors
            return

        try:
            if options['action'] == 'add':
                try:
                    added = self.queue_add(title=options['title'], imdb_id=options['imdb_id'],
                        quality=options['quality'], force=options['force'])
                except QueueError, e:
                    console(e.message)
                    if e.errno == 1:
                        # This is an invalid quality error, display some more info
                        console('Recognized qualities are %s' % ', '.join([qual.name for qual in qualities.all()]))
                        console('ANY is the default and can also be used explicitly to specify that quality should be ignored.')
                else:
                    console('Added %s to queue with quality %s' % (added['title'], added['quality']))
            elif options['action'] == 'del':
                try:
                    title = self.queue_del(options['imdb_id'])
                except QueueError, e:
                    console(e.message)
                else:
                    console('Removed %s from queue' % title)
        except OperationalError:
            log.critical('OperationalError')

    # TODO: a bit useless?
    def error(self, msg):
        console('IMDb Queue error: %s' % msg)

    def validate_quality(self, quality):
        # Check that the quality is valid
        # Make sure quality is in the format we expect
        if quality.upper() == 'ANY':
            return 'ANY'
        elif qualities.get(quality, False):
            return qualities.common_name(quality)
        else:
            raise QueueError('ERROR! Unknown quality `%s`' % quality, errno=1)

    def queue_add(self, title=None, imdb_id=None, quality='ANY', force=True):
        """Add an item to the queue with the specified quality"""

        if not title or not imdb_id:
            # We don't have all the info we need to add movie, do a lookup for more info
            result = self.parse_what(imdb_id or title)
            title = result['title']
            imdb_id = result['imdb_id']
        quality = self.validate_quality(quality)

        session = Session()

        # check if the item is already queued
        item = session.query(QueuedMovie).filter(QueuedMovie.imdb_id == imdb_id).first()
        if not item:
            #TODO: fix
            item = QueuedMovie(imdb_id=imdb_id, quality=quality, immortal=force, title=title)
            session.add(item)
            session.commit()
            session.close()
            return {'title': title, 'imdb_id': imdb_id, 'quality': quality, 'force': force}
        else:
            raise QueueError('ERROR: %s is already in the queue' % title)

    def queue_del(self, imdb_id):
        """Delete the given item from the queue"""

        session = Session()
        # check if the item is queued
        item = session.query(QueuedMovie).filter(QueuedMovie.imdb_id == imdb_id).first()
        if item:
            title = item.title
            session.delete(item)
            session.commit()
            return title
        else:
            raise QueueError('%s is not in the queue' % imdb_id)

    def queue_edit(self, imdb_id, quality):
        """Change the required quality for a movie in the queue"""
        self.validate_quality(quality)
        session = Session()
        # check if the item is queued
        item = session.query(QueuedMovie).filter(QueuedMovie.imdb_id == imdb_id).first()
        if item:
            item.quality = quality
            session.commit()
            return item.title
        else:
            raise QueueError('%s is not in the queue' % imdb_id)

    def queue_list(self):
        """List IMDb queue"""

        items = self.queue_get()
        console('-' * 79)
        console('%-9s %-9s %-36s %-15s %s' % ('IMDB id', 'TMDB id', 'Title', 'Quality', 'Force'))
        console('-' * 79)
        for item in items:
            console('%-9s %-9s %-45s %-15s %s' % (item.imdb_id, item.tmdb_id, item.title, item.quality, item.immortal))

        if not items:
            console('Movie queue is empty')

        console('-' * 79)

    def queue_get(self):
        """Get the current IMDb queue.
        Returns:
        List of QueuedMovie objects (detached from session)
        """
        session = Session()
        try:
            items = session.query(QueuedMovie).all()
            for item in items:
                if not item.title:
                    # old database does not have title / title not retrieved
                    try:
                        item.title = self.parse_what(item.imdb_id)['title']
                    except QueueError:
                        item.title = 'N/A'
            return items
        finally:
            session.close()


register_plugin(FilterMovieQueue, 'movie_queue', api_ver=2)

register_plugin(MovieQueueManager, 'movie_queue_manager', builtin=True)
register_parser_option('--movie-queue', action='callback',
                       callback=MovieQueueManager.optik_imdb_queue,
                       help='(add|del|list) [IMDB_URL|NAME] [QUALITY]')
