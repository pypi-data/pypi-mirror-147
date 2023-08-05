var term = new Terminal();
term.open(document.getElementById('terminal'));

var shellprompt = '$ ';
term.prompt = function () {
  term.write('\r\n' + shellprompt);
};

term.clearPrompt = function() {
  term.write('\r')
  term.clear()
  term.writeln('\x1B[1;3;31mLfnt workstation\x1B[0m')
  term.prompt();
  term.setOption('cursorBlink', true);
}

var cmd = '';
term.clearPrompt()
term.onKey(e => {
    const printable = !e.domEvent.altKey && !e.domEvent.altGraphKey && !e.domEvent.ctrlKey && !e.domEvent.metaKey;

    if (e.domEvent.keyCode === 13) {
        console.log("cmd " + cmd)
        if(cmd === 'clear' || cmd === "reset")
        {
          term.clearPrompt()
        } else {
          // run command
          term.prompt()
        }
        cmd = '';
    } else if (e.domEvent.keyCode === 8) {
        // Do not delete the prompt
        if (term._core.buffer.x > 2) {
            term.write('\b \b');
        }
    } else if (printable) {
        term.write(e.key);
        cmd += e.key;
    } else if ( e.key === '\f') {
      term.clearPrompt()
      term.write(cmd);
    } else if ( e.key === '\x03') {
      term.write('^C\r\n');
      cmd = ''
      term.prompt()
    } else if ( e.key === '\x04' && cmd === '') {
      term.write('^D\r\n');
      cmd = ''
      term.prompt()
    } else {
      console.log(e);
    }
});
