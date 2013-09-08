define(['jquery', 'underscore'], function ($, _) {

  return {

    parseErrors: function (xhr) {
      var errors, note
      try {
        errors = $.parseJSON(xhr.responseText);
      } catch (e) {
        note = _.has(xhr, 'status') ? xhr.status : ''
        if (_.has(xhr, 'statusText')) note += ' ' + xhr.statusText
        errors = [{note: note || 'Application error'}]
      }
      return errors
    }

  }

})
