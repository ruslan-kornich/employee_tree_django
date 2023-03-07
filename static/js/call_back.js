var getJSON = function (url, callback, obj) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function () {
        var status = xhr.status;
        if (status === 200) {
            callback(null, xhr.response, obj);
        } else {
            callback(status, xhr.response, obj);
        }
    };
    xhr.send();
};