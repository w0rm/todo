define([ 'backbone'
       , 'models/todo'
       ], function (Backbone, TodoModel) {

  return Backbone.Collection.extend({
    model: TodoModel
  , url: '/api/todos'
  })

})
