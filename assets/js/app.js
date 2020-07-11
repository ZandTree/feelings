var csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        headers: {"X-CSRFToken": csrftoken}
    });
