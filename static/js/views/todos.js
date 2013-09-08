define([ 'backbone'
       , 'underscore'
       , 'utils'
       , 'views/todo'
       , 'text!templates/todos.html'
       ], function (Backbone, _, utils, TodoView, todosTemplate) {

  return Backbone.View.extend({

    el: 'body'

  , events: {
      'submit .js-create-form': 'createTodo'
    }

  , template: _.template(todosTemplate)

  , initialize: function () {
      this.listenTo(this.collection, {
        reset: this.render,
        add: this.renderTodo
      })
    }

  , render: function () {
      this.$el.html(this.template({collection: this.collection}))
      this.$todos = this.$('.js-todos')
      this.collection.each(this.renderTodo, this)
      return this;
    }

  , renderTodo: function (todo) {
      var todoView = new TodoView({model: todo})
      this.$todos.prepend(todoView.render().el)
    }

  , createTodo: function (e) {
      e.preventDefault()
      this.collection.create(
        {content: this.$('.js-create-form [name="content"]').val()}
      , { wait: true
        , error: _.bind(this.showError, this)
        , success: _.bind(this.emptyForm, this)
        }
      )
    }

  , showError: function (todos, xhr) {
      var errors = utils.parseErrors(xhr)
      this.$('.js-create-error')
        .html(_.map(errors, function (e) {return e.note}).join('<br>'))
        .removeClass('is-hidden')
    }

  , emptyForm: function () {
      this.$('.js-create-error').empty().addClass('is-hidden')
      this.$('.js-create-form').trigger('reset')
      this.$('.js-create-form [name="content"]').focus()
    }

  })

})
