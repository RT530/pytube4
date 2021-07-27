from selenium.webdriver import Chrome, ChromeOptions
from chromedriver_autoinstaller import install
from .streams import Streams, Stream


class YouTube:
    def __init__(self, url, progress=None):
        assert 'watch?v=' in url, 'URL format should be https://www.youtube.com/watch?v=<v_id>'
        self._v_id = url.split('watch?v=')[1]
        if '&' in self._v_id:
            self._v_id = self._v_id.split('&')[0]

        self._progress = progress
        self._info = self._get_data()
        self._title = self._info['title']

    def _get_data(self):
        install()
        options = ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        driver = Chrome(options=options)
        driver.get(f'https://www.youtube.com/watch?v={self._v_id}')
        driver.execute_script(
            'var jquery = document.createElement("script");'
            'jquery.src = "https://code.jquery.com/jquery-3.2.1.min.js";'
            'document.body.appendChild(jquery);'
        )
        while driver.execute_script('return typeof(jQuery)=="undefined"'):
            pass
        data = driver.execute_script('''
            function parse_decsig(data) {
                var fnnameresult = /=([a-zA-Z0-9\$]+?)\(decodeURIComponent/.exec(data)
                var fnname = fnnameresult[1]
                var _argnamefnbodyresult = new RegExp(escape_reg_exp(fnname) + '=function\\\((.+?)\\\){(.+?)}').exec(data)
                var [_, argname, fnbody] = _argnamefnbodyresult
                var helpernameresult = /;(.+?)\..+?\(/.exec(fnbody)
                var helpername = helpernameresult[1]
                var helperresult = new RegExp('var ' + escape_reg_exp(helpername) + '={[\\\s\\\S]+?};').exec(data)
                var helper = helperresult[0]
                return new Function([argname], helper + '\\n' + fnbody)
            }

            function escape_reg_exp(text) {
                return text.replace(/[.*+?^${}()|[\]\\\]/g, '\\\$&')
                    }

            var title
            var adaptive
            var script = $('script')
            $.ajaxSetup({ async: false })
            for (var i = 0; i < script.length; i++) {
                if (script[i].src.indexOf('base.js') != -1) {
                    $.get(script[i].src, (text) => {
                        var decsig = parse_decsig(text)
                        var player_response = window.ytplayer.config.args.raw_player_response
                        adaptive = player_response.streamingData.adaptiveFormats.map(x =>
                            Object.assign({}, x, [...new URLSearchParams(x.cipher || x.signatureCipher).entries()].reduce((acc, [k, v]) => ((acc[k] = v), acc), {}))
                        )
                        for (var obj of adaptive) {
                            if (obj.s) {
                                obj.s = decsig(obj.s)
                                obj.url += `&${obj.sp}=${escape_reg_exp(obj.s)}`
                            }
                        }
                        var details = player_response.videoDetails
                        title = details['title']
                    })
                    break
                }
            }
            return {
                title: title,
                adaptive: adaptive
            }
        ''')
        driver.close()
        return data

    @property
    def streams(self):
        return Streams([Stream(data, self._title, self._progress) for data in self._info['adaptive']])
