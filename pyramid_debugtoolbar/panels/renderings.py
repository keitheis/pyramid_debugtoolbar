from pprint import pformat

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from pyramid_debugtoolbar.panels import DebugPanel
from pyramid_debugtoolbar.utils import dictrepr

_ = lambda x: x


#class CodeHtmlFormatter(HtmlFormatter):
    #def wrap(self, source, outfile):
        #return self._wrap_code(source)

    #def _wrap_code(self, source):
        #for i, t in source:
            #if t.startswith("u'"):
                #t2 = t[2:-1]
                #t = t2.decode('unicode-escape')
            #yield i, t


class RenderingsDebugPanel(DebugPanel):
    """
    Panel that displays the renderers (templates and 'static' renderers such
    as JSON) used during a request.
    """
    name = 'Template'
    renderings = ()
    template = 'pyramid_debugtoolbar.panels:templates/renderings.dbtmako'

    @property
    def has_content(self):
        return bool(self.renderings)

    def process_beforerender(self, event):
        if not self.renderings:
            self.renderings = []
        name = event['renderer_info'].name
        if name and name.startswith('pyramid_debugtoolbar'):
            return
        val = getattr(event, 'rendering_val', '<unknown>')
        try:
            val = pformat(val, width=160)
            lexer = get_lexer_by_name("python")
            formatter = HtmlFormatter(linenos=False, cssclass="source")
            #formatter = CodeHtmlFormatter(linenos=False, cssclass="source")
            val = highlight(val, lexer, formatter)
        except:
            # crazyass code raises an exception during __repr__ (formish)
            val = '<unknown>'
        self.renderings.append(dict(name=name,
                                    system=dictrepr(event),
                                    val=val))

    def nav_title(self):
        return _('Renderers')

    def nav_subtitle(self):
        num = len(self.renderings)
        return '%d' % (num)

    def title(self):
        return _('Renderers')

    def url(self):
        return ''

    def process_response(self, response):
        self.data = {'renderings': self.renderings}
