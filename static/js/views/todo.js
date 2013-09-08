define([ 'jquery'
       , 'backbone'
       , 'underscore'
       , 'utils'
       , 'text!templates/todo.html'
       ], function ($, Backbone, _, utils, todoTemplate) {

  return Backbone.View.extend({

    tagName: 'li'
  , className: 'todo'
  , events: {
      'click .js-remove': 'removeTodo'
    , 'click .js-edit': 'editTodo'
    , 'click .js-cancel': 'cancelEdit'
    , 'change [name="is_done"]': 'saveDone'
    , 'submit .js-edit-form': 'saveContent'
    }
  , template: _.template(todoTemplate)

  , initialize: function () {
      this.listenTo(this.model, {
        remove: this.remove
      , change: this.render
      , error: this.showError
      })
    }

  , render: function () {
      this.$el.removeClass('is-edit').html(this.template({todo: this.model}))
      return this
    }

  , removeTodo: function (e) {
      e.preventDefault()
      this.model.destroy()
    }

  , editTodo: function (e) {
      e.preventDefault()
      this.$el.addClass('is-edit')
      this.$('[name="content"]').focus()
    }

  , cancelEdit: function (e) {
      e.preventDefault()
      this.render()
    }

  , saveDone: function (e) {
      this.model.save(
        {is_done: this.$('[name="is_done"]').is(':checked')}
      , {wait: true}
      )
    }

  , saveContent: function (e) {
      e.preventDefault()
      this.model.save(
        {content: this.$('[name="content"]').val()}
      , {wait: true}
      )
    }

  , showError: function (todo, xhr) {
      var errors = utils.parseErrors(xhr)
      this.$('.js-edit-error')
        .html(_.map(errors, function (e) {return e.note}).join('<br>'))
        .removeClass('is-hidden')
    }

  })

})
