def CommentSchema(*args, **kwargs):
    """
    NOTE: The CommentSchema schema requires the
    required_one_or_another_factory('solution_id', 'parent_id') validator to be
    passed into its constructor:
    ... validator = required_one_or_another_factory('solution_id', 'parent_id')
    ... comment_schema = CommentSchema(validator=validator)
    This is in order to verify that either the solution_id XOR parent_id is set.
    """

    comment_schema = SchemaNode(Mapping(*args, **kwargs))

    class CommentsSchema(SequenceSchema):
        comment = comment_schema

    comment_schema.add(SchemaNode(Int(), missing=None, name='solution_id'))
    comment_schema.add(SchemaNode(Int(), missing=None, name='parent_id'))
    comment_schema.add(CommentRevisionsSchema(missing=None, name='revisions'))
    comment_schema.add(CommentVotesSchema(missing=None, name='votes'))
    comment_schema.add(CommentsSchema(missing=None, name='replies'))
    return comment_schema

DOES THIS:
>>> schema.deserialize({'solution_id':0, 'parent_id':0, 'replies': [{'solution_id':0, 'parent_id':0, 'replies': [{'solution_id':0, 'parent_id':0, 'replies':[]}]}]})
{'parent_id': 0, 'votes': None, 'replies': [{'parent_id': 0, 'votes': None, 'replies': [{'parent_id': 0, 'votes': None, 'replies': [], 'solution_id': 0, 'revisions': None}], 'solution_id': 0, 'revisions': None}], 'solution_id': 0, 'revisions': None}
