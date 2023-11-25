showdown.extension('highlight',
    ({ pre = false, auto_detection = true } = {}) => {
        const classAttr = 'class="';

        const filter = (text, converter, options) => {
            const params = {
                left: "<pre><code\\b[^>]*>"
              , right: "</code></pre>"
              , flags: "g"
            }

            const htmlDecode = (text) => {
                return (
                text
                    .replace(/&amp;/g, '&')
                    .replace(/&lt;/g, '<')
                    .replace(/&gt;/g, '>')
                );
            }

            const replacement = (wholeMatch, match, left, right) => {
                match = htmlDecode(match)

                const lang = (left.match(/class=\"([^ \"]+)/) || [])[1]

                if (!lang && !auto_detection) {
                    return wholeMatch
                }

                if (left.includes(classAttr)) {
                    const attrIndex = left.indexOf(classAttr) + classAttr.length
                    left = left.slice(0, attrIndex) + 'hljs ' + left.slice(attrIndex)
                } else {
                    left = left.slice(0, -1) + ' class="hljs">'
                }

                if (pre && lang) {
                    left = left.replace('<pre>', `<pre class="${lang} language-${lang}">`)
                }

                if (lang && hljs.getLanguage(lang)) {
                    return left + hljs.highlight(match, { language: lang }).value + right
                }

                return left + hljs.highlightAuto(match).value + right
            }

            return showdown.helper.replaceRecursiveRegExp(
                text,
                replacement,
                params.left,
                params.right,
                params.flags
            )
        }

        return [
            {
                type: "output"
              , filter
            }
        ]
    }
);

const converter = new showdown.Converter({extensions: ['highlight']});
