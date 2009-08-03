var LOAD_RULES_URL = '/ajax/load-rules';

$(document).ready(function() {
  $('#try-rules').click(function() {
    alert('Not yet implemented.');
    return false;
  });
  $('#load-rules').click(function() {
    var name = $('#rules-name').val();
    $.getJSON(LOAD_RULES_URL, {name: name}, setNewRules);
    return false;
  });
  $('input').change(scheduleContentRefresh);
});

function setNewRules(rules_json, text_status) {
  if (text_status != 'success')
    alert('Got ' + text_status);

  $('input, textarea').each(function() {
    var input_name = $(this).attr('name');
    if (input_name in rules_json)
      $(this).val(rules_json[input_name]);
  });
}

/////// This part here is not yet useful (as of 2 August 2009).

// Javascript timeout. It will refresh the content on this page when it fires.
var content_refresh_timeout = null;

/**
 * Schedules the refresh of all the content on this page due to user
 * interaction. Content is scheduled to be refresed 2 seconds after the last
 * user interaction.
 */
function scheduleContentRefresh() {
  if (content_refresh_timeout)
    clearTimeout(content_refresh_timeout);
  content_refresh_timer = setTimeout(function() {
    content_refresh_timeout = null;
    refreshContent()
  }, 2000);
}

/**
 * Refreshes (or loads for the first time) the content on this page based on
 * user input.
 */
function refreshContent() {
}