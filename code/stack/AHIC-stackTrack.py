class stack_track:

  def __init__(self):
    self.previous = False
    self.pprevious = False
    self.ptype = None
    self.pptype = None
    self.previous_height = 0
    self.pprevious_height = 0
    self.scale = 0
    self.previous_scale = 0
    self.object_order = []
    self.total_width = 0
    self.organized_objects = []
    self.current_offset = 0
    self.previous_offset = 0
    self.previous_scale_height = 0

  def adjust_stackit(self, previous):
    """ Stack the next object? """
    self.previous = self.pprevious
    self.pprevious = previous

  def check_previous(self):
    if self.previous:
      return True
    else:
      return False

  def adjust_height(self, height):
    """ Send the height """
    self.previous_height = self.pprevious_height
    self.pprevious_height = height

  def get_this_left_offset(self):
    return round(self.previous_offset, 2)

  def adjust_left_offset(self, offset_width, position, next_width):
    if position == 'GS':
      offset_width = offset_width / 2.0 - next_width
    else:
      next_width = 0
    self.previous_offset = self.current_offset
    self.current_offset += offset_width

  def offset_height(self):
    if self.previous:
      return floor(self.previous_height)
    else:
      return 0

  def set_previous_scale(self, scale):
    self.previous_scale = scale

  def track(self, keyword_reasoning_object):
    # trackers = {
    #   "GS" : self.ground_surface_objects,
    #   "GG" : self.ground_objects,
    #   "SS" : self.surface_objects,
    #   "WW" : self.wall_objects,
    # }
    # trackers[position].append(keywordImage)
    # check previous, if it was a ground surface object, and this is a surface object - stack it
    k = keyword_reasoning_object
    ki = k.keywordImage
    position = ki.position
    if position == 'GS':
      r = True
    else:
      r = False
    self.adjust_stackit(r)
    if position in ['GS', 'GG', 'WW']:
      self.previous = False
    self.adjust_height(ki.image.height * float(ki.scale))
    # self.object_order.append([self.check_previous(), keywordImage]) # [Boolean:stackit?, keywordImage]
    self.object_order.append({
      'stackit': self.check_previous(),
      'keywordImage': ki,
      'offset_height': self.offset_height(),
      'keyword': k.keyword,
      'main_keyword': ki.name,
      'reasoning': k.reason,
      'this_museum': k.museum,
      'image': ki.image,
      'scale': ki.scale,
      'position': position,
      })
    self.total_width += ki.image.width * float(ki.scale)

  def track_solo(self, keywordImage):
    ki = keywordImage
    position = ki.position
    if position == 'GS':
      r = True
    else:
      r = False
    self.adjust_stackit(r)
    if position in ['GS', 'GG', 'WW']:
      self.previous = False
    self.adjust_height(ki.image.height * float(ki.scale))
    self.object_order.append({
      'stackit': self.check_previous(),
      'keywordImage': ki,
      'keyword': ki.name,
      'offset_height': self.offset_height,
      'main_keyword': ki.name,
      'image': ki.image,
      'this_museum': None,
      'scale': ki.scale,
      'position': position,
      })
    self.total_width += ki.image.width * float(ki.scale)

  def get_this_width(self, width):
    return round(float(width) / self.total_width * 100, 2)

  def get_this_height(self, o):
    scale = o['scale']
    height = o['keywordImage'].image.height
    position = o['position']
    previous_height = self.previous_height
    previous_scale = self.previous_scale
    if position == 'WW':
      height = 130 * float(scale)
    elif position == 'SS':
      height = 200
    else:
      height = 150 * float(scale)
    self.previous_scale_height = height
    return height

  def organize(self):
    # print 'object order: ', self.object_order
    # objects = [[k[1], self.object_order[self.object_order.index([True, k[1]])-1][1]] for k in self.object_order if k[0]]
    # print "objects: ", objects
    self.organized_objects = []
    for i, o in enumerate(self.object_order):
      # print "newtmp: ", newtemp
      # newtmp += {
      #   'width': self.get_this_width(o['keywordImage'].image.width*o['keywordImage'].scale),
      #   'previous_height': o['offset_height'],
      # }
      o['width'] = self.get_this_width(o['keywordImage'].image.width
                                       * o['keywordImage'].scale)
      if i >= len(self.organized_objects):
        next_width = 0
      elif i < 1:
        next_width = 0
      else:
        next_width = self.organized_objects[i + 1]['width']
      self.adjust_left_offset(float(o['width']), o['keywordImage'].position,
                              next_width)
      o['offset_left'] = self.get_this_left_offset()

      o['scalewidth'] = o['width'] * float(o['scale'])

      o['previous_height'] = o['keywordImage'].image.height / 100 \
        * o['scalewidth']

      # o['scaleheight'] = 150 * float(o['scale'])#o['keywordImage'].image.height*float(o['scale'])
      o['previous_scale_height'] = self.previous_scale_height
      o['previous_scale'] = self.previous_scale
      o['scaleheight'] = self.get_this_height(o)
      # # print "museum: ", o['keywordImage'].museum
      self.organized_objects.append(o)

    # print 'objects: ', self.organized_objects

  def get_trackers(self):
    return [self.ground_surface_objects, self.ground_objects,
            self.surface_objects, self.wall_objects]

  def get_organized(self):
    return self.organized_objects

  def get_surface_objects(self):
    objects = self.organized_objects
    for o in objects:
      if o['position'] == 'SS':
        yield o

  def get_ground_objects(self):
    objects = self.organized_objects
    for o in objects:
      if o['keywordImage'].is_surface():
        yield o

  def get_objects_of_type(self, obj_type):
    objects = self.organized_objects
    ff = 'is_' + obj_type
    for o in objects:
      if getattr(o['keywordImage'], ff)():
        yield o

  def set_total_width(self):
    objects = self.organized_objects
    total_width = 0
    for o in objects:
      width = o['keywordImage'].image.width
      scale = o['keywordImage'].scale
      total_width += width * scale
    self.total_width = total_width
  def get_total_width(self):
    return self.total_width
