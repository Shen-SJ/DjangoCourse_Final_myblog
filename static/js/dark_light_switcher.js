function onclik(event) {
    toggle_dark_light()
}

function toggle_dark_light() {
    const DARK_CLASS = 'dark-theme';
    const FLAT_CLASS ='flat-theme'

    let body = document.querySelector("body");

    if (body.id===DARK_CLASS) {
        setCookie('_theme', 'flat');
        body.id = FLAT_CLASS;
    } else {
        setCookie('_theme', 'dark');
        body.id = DARK_CLASS;
    }
}

function setCookie(name, value, days) {
    let d = new Date;
    d.setTime(d.getTime() + 24*60*60*1000*days);
    document.cookie = name + "=" + value + ";path=/;SameSite=strict;expires=" + d.toGMTString();
}