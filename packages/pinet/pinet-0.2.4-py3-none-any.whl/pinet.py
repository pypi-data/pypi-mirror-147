import warnings
class tag:
    def __init__(self ,tag_name=None ,name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
        self.tag_name = tag_name
        self.name = name
        self.id = id
        self.clas = clas
        self.style = style
        self.accesskey = accesskey
        self.draggable = draggable
        self.hidden = hidden

    def extra_attributes(self):
        return ""

    def __render_list(self, data):
        ans=""
        for i in data:
            ans+=i
        return ans

    def render(self, *values):
        assert self.tag_name is not None
        assert self.draggable in ['true','false',None]
        return f'''<{self.tag_name}{' name="'+self.name+'"' if self.name is not None else ""}{' id="'+self.id+'"' if self.id is not None else ""}{' class="'+self.clas+'"' if self.clas is not None else ""}{' style="'+self.style+'"' if self.style is not None else ""}{' draggable="'+self.draggable+'"' if self.draggable is not None else ""}{' accesskey="'+self.accesskey+'"' if self.accesskey is not None else ""}{self.extra_attributes()}{' hidden' if self.hidden else ""}>{self.__render_list(values)}</{self.tag_name}>'''

def export_html(data, fileName):
    file = open(fileName, 'w')
    file.write(data)

class html:
    def __init__(self, title=None):
        self.title = title
        self.head = ""

    def add_link(self, link):
        assert type(link) is html.link, 'Link in function should be of type html.link'
        self.head += link.render()

    def __render_list(self, data):
        ans=""
        for i in data:
            ans+=i
        return ans

    def render(self, *content):
        assert self.title is not None, 'Please enter some title for the Web application'
        return f'''<!DOCTYPE html><html><head><title>{self.title}</title>{self.head}</head><body>{self.__render_list(content)}</body></html>'''

    class a(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, href=None, referrerpolicy=None, type=None, rel=None, ping=None, draggable=None, download=None, target=None, hidden=False):
            super().__init__('a',name, id, clas, style, accesskey, draggable, hidden)
            assert referrerpolicy in ['no-referrer','no-referrer-when-downgrade','origin','origin-when-cross-origin','same-origin','strict-origin-when-cross-origin','unsafe-url', None], f'Invalid referrerpolicy: {referrerpolicy}'
            assert rel in ['alternate','author','bookmark','external','help','license','next','nofollow','noopener','noreferrer','prev','search','tag', None], f'Invalid rel: {rel}'
            assert target in ['_blank','_parent','_self','_top',None], f'Invalid target: {target}'
            self.href = href
            self.download = download
            self.ping = ping
            self.referrerpolicy = referrerpolicy
            self.type = type
            self.target = target
            self.rel = rel

        def extra_attributes(self):
            return f'''{' href="'+self.href+'"' if self.href is not None else ""}{' download="'+self.download+'"' if self.download is not None else ""}{' ping="'+self.ping+'"' if self.ping is not None else ""}{' type="'+self.type+'"' if self.type is not None else ""}{' target="'+self.target+'"' if self.target is not None else ""}{' referrerpolicy="'+self.referrerpolicy+'"' if self.referrerpolicy is not None else ""}{' rel="'+self.rel+'"' if self.rel is not None else ""}'''

    class abbr(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('abbr',name, id, clas, style, accesskey, draggable, hidden)

    class address(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('address',name, id, clas, style, accesskey, draggable, hidden)

    class aside(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('cle',name, id, clas, style, accesskey, draggable, hidden)

    class audio(tag):
        def __init__(self, autoplay=None, controls=None, loop=None, muted=None, preload=None, type=None, src=None):
            assert preload in ["auto","metadata","none",None], f'''Invalid attribute: {preload}'''
            self.autoplay = autoplay
            self.controls = controls
            self.loop = loop
            self.muted = muted
            self.preload = preload
            self.type = type
            self.src = src

        def render(self):
            return f'''<audio{' src="'+self.src+'"' if self.src is not None else ""}{' type="'+self.type+'"' if self.type is not None else ""}{ 'autoplay' if self.autoplay else ""}{ 'controls' if self.controls else ""}{ 'loop' if self.loop else ""}{ 'muted' if self.muted else ""}{ 'preload' if self.preload else ""}/>'''

    class b(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('b',name, id, clas, style, accesskey, draggable, hidden)

    class base(tag):
        def __init__(self, href=None, target=None):
            assert target in ['__blank','__parent','__self','__top',None], f'''Invalid attribute: {target}'''
            self.href = href
            self.target = target

        def extra_attributes(self):
            return f'''{' href="'+self.href+'"' if self.href is not None else ""}{' target="'+self.target+'"' if self.target is not None else ""}'''

        def render(self):
            return f'''<base{self.extra_attributes()}>'''

    class bdi(tag):
        def __init__(self, dir=None):
            assert dir in ['ltr','rtl',None], f'''Invalid attribute: {dir}'''
            self.dir = dir

        def extra_attributes(self):
            return f'''{' dir="'+self.dir+'"' if self.dir is not None else ""}'''

        def render(self):
            return f'''<base{self.extra_attributes()}>'''

    class blockquote(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, cite=None):
            super().__init__('a',name, id, clas, style, accesskey, draggable)
            self.cite = cite

        def extra_attributes(self):
            return f'''{' cite="'+self.cite+'"' if self.cite is not None else ""}'''

    class br(tag):
        def render(self):
            return '''<br>'''

    class caption(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('caption',name, id, clas, style, accesskey, draggable, hidden)

    class cite(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('cite',name, id, clas, style, accesskey, draggable, hidden)

    class code(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('code',name, id, clas, style, accesskey, draggable, hidden)

    class data(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, value=None, draggable=None, hidden=False):
            super().__init__('data',name, id, clas, style, accesskey, draggable, hidden)
            assert value is not None, 'Value attribute must not be None'
            self.value = value

        def extra_attributes(self):
            return f'''{' value="'+self.value+'"' if self.value is not None else ""}'''

    class datalist(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False, values=None):
            super().__init__('datalist',name, id, clas, style, accesskey, draggable, hidden)
            self.values = values

        def __render_list(self, data):
            ans=""
            for i in data:
                ans+=f'''<option value="{i}">'''
            return ans

        def render(self):
            return super().render(self.__render_list(self.values))

    class delete(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('del',name, id, clas, style, accesskey, draggable, hidden)

    class details(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('details',name, id, clas, style, accesskey, draggable, hidden)

    class dfn(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('dfn',name, id, clas, style, accesskey, draggable, hidden)

    class div(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('div',name, id, clas, style, accesskey, draggable, hidden)

    class em(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('em',name, id, clas, style, accesskey, draggable, hidden)

    class embed(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, height=None, width=None, src=None, type=None):
            warnings.warn("Its suggested to use specific tags for media instead of embed")
            super().__init__('embed',name, id, clas, style, accesskey, draggable)
            self.height = height
            self.width = width
            self.src = src
            self.type = type
        def extra_attributes(self):
            return f'''{' src="'+str(self.src)+'"' if self.src is not None else ""}{' type="'+str(self.type)+'"' if self.type is not None else ""}{' width="'+str(self.width)+'"' if self.width is not None else ""}{' height="'+str(self.height)+'"' if self.height is not None else ""}'''

    class figcaption(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('figcaption',name, id, clas, style, accesskey, draggable, hidden)

    class footer(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('footer',name, id, clas, style, accesskey, draggable, hidden)

    class form(tag):
        def __init__(self, action=None, method=None, rel=None):
            super().__init__(tag_name='form')
            assert rel in ["external","help","license","next","nofollow","noopener","noreferrer","opener","prev","search", None], f'''Invalid rel: {rel}'''
            assert method in ['POST','GET',None], f'''Invalid method: {method}'''
            self.action = action
            self.method = method
            self.rel = rel

        def extra_attributes(self):
            return f'''{' action="'+self.action+'"' if self.action is not None else ""}{' method="'+self.method+'"' if self.method is not None else ""}{' rel="'+self.rel+'"' if self.rel is not None else ""}'''

    class h1(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('h1',name, id, clas, style, accesskey, draggable, hidden)

    class h2(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('h2',name, id, clas, style, accesskey, draggable, hidden)

    class h3(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('h3',name, id, clas, style, accesskey, draggable, hidden)

    class h4(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('h4',name, id, clas, style, accesskey, draggable, hidden)

    class h5(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('h5',name, id, clas, style, accesskey, draggable, hidden)

    class h6(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('h6',name, id, clas, style, accesskey, draggable, hidden)

    class hr(tag):
        def render(self):
            return '''<hr>'''

    class i(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('i',name, id, clas, style, accesskey, draggable, hidden)

    class input(tag):
        def __init__(self, type="text", value=None, name=None, id=None, clas=None, align=None, style=None, accesskey=None, draggable=None, alt=None, width=None):
            assert type in ['button','checkbox','color','date','datetime-local','email','file','hidden','image','month','number','password','radio','range','reset','search','submit','tel','text','time','url','week'], f'''Invalid input type: {type}'''
            super().__init__('input',name, id, clas, style, accesskey, draggable)
            self.type = type
            self.value = value
            self.alt = alt
            self.width = width

        def extra_attributes(self):
            return f'''{' type="'+self.type+'"' if self.type is not None else ""}{' width="'+self.width+'"' if self.width is not None else ""}{' alt="'+self.alt+'"' if self.alt is not None else ""}'''

        def render(self):
            return f'''<{self.tag_name}{' value="'+self.value+'"' if self.value is not None else ""}{' name="'+self.name+'"' if self.name is not None else ""}{' id="'+self.id+'"' if self.id is not None else ""}{' class="'+self.clas+'"' if self.clas is not None else ""}{' style="'+self.style+'"' if self.style is not None else ""}{' draggable="'+self.draggable+'"' if self.draggable is not None else ""}{' accesskey="'+self.accesskey+'"' if self.accesskey is not None else ""}{self.extra_attributes()}/>'''

    class ins(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('ins',name, id, clas, style, accesskey, draggable, hidden)

    class kbd(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('kbd',name, id, clas, style, accesskey, draggable, hidden)

    class label(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, label_for=None, draggable=None, form=None):
            super().__init__('label',name, id, clas, style, accesskey, draggable)
            self.label_for = label_for
            self.form = form

        def extra_attributes(self, href=None):
            return f'''{' for="'+self.label_for+'"' if self.label_for is not None else ""}{' form="'+self.form+'"' if self.form is not None else ""}'''

    class main(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('main',name, id, clas, style, accesskey, draggable, hidden)

    class mark(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('mark',name, id, clas, style, accesskey, draggable, hidden)

    class meter(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False, high=None, low=None, max=None, min=None, value=None, optimum=None):
            super().__init__('meter',name, id, clas, style, accesskey, draggable, hidden)
            self.high = high
            self.low = low
            self.min = min
            self.max = max
            self.value = value
            self.optimum = optimum

        def extra_attributes(self):
            return f'''{' high="'+str(self.high)+'"' if self.high is not None else ""}{' low="'+str(self.low)+'"' if self.low is not None else ""}{' min="'+str(self.min)+'"' if self.min is not None else ""}{' max="'+str(self.max)+'"' if self.max is not None else ""}{' value="'+str(self.value)+'"' if self.value is not None else ""}{' optimum="'+str(self.optimum)+'"' if self.optimum is not None else ""}'''

    class noscript(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('noscript',name, id, clas, style, accesskey, draggable, hidden)

    class nav(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None):
            super().__init__('nav',name, id, clas, style, accesskey, draggable)

    class p(tag):
        def __init__(self, name=None, id=None, clas=None, align=None, style=None, accesskey=None, draggable=None):
            super().__init__('p',name, id, clas, style, accesskey, draggable)
            self.align = align

        def extra_attributes(self):
            assert self.align in ["left","right","center","justify",None], f'''Invalid attribute: {self.align}'''
            return f'''{' align="'+self.align+'"' if self.align is not None else ""}'''

    class link(tag):
        def __init__(self, rel=None, href=None, type=None, referrerpolicy=None):
            assert referrerpolicy in ["no-referrer","no-referrer-when-downgrade","origin","origin-when-cross-origin","unsafe-url",None], f'''Invalid referrerpolicy: {referrerpolicy}'''
            assert rel in ["alternate","author","dns-prefetch","help","icon","license","next","pingback","preconnect","prefetch","preload","prerender","prev","search","stylesheet",None], f'''Invalid rel: {rel}'''
            self.rel = rel
            self.href = href
            self.type = type
            self.referrerpolicy = referrerpolicy

        def render(self):
            return f'''<link{' rel="'+self.rel+'"' if self.rel is not None else ""}{' href="'+self.href+'"' if self.href is not None else ""}{' type="'+self.type+'"' if self.type is not None else ""}{' referrerpolicy="'+self.referrerpolicy+'"' if self.referrerpolicy is not None else ""}>'''

    class legend(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None):
            super().__init__('legend',name, id, clas, style, accesskey, draggable)

    class pre(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None):
            super().__init__('pre',name, id, clas, style, accesskey, draggable)

    class q(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None):
            super().__init__('q',name, id, clas, style, accesskey, draggable)

    class s(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None):
            super().__init__('s',name, id, clas, style, accesskey, draggable)

    class sup(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('sup',name, id, clas, style, accesskey, draggable, hidden)

    class sub(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('sub',name, id, clas, style, accesskey, draggable, hidden)

    class small(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('small',name, id, clas, style, accesskey, draggable, hidden)

    class span(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('h1',name, id, clas, style, accesskey, draggable, hidden)

    class strong(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('strong',name, id, clas, style, accesskey, draggable, hidden)

    class table(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False, headers=[], cols=[]):
            assert isinstance(headers,list), 'Headers are expected to be list'
            assert isinstance(cols,list), 'Rows are expected to be list of lists'
            super().__init__('strong',name, id, clas, style, accesskey, draggable, hidden)
            self.cols = cols
            self.headers = headers

        def __render_table(self):
            ans = ""
            if self.headers!=[] :
                ans+="<thead>"
                for head in self.headers:
                    ans+="<tr>"+head+"</tr>"
                ans+="</thead>"
            if self.cols != []:
                for i in self.cols:
                    ans+="<tr>"
                    for j in i:
                        ans+="<td>"+str(j)+"<td>"
                    ans+="</tr>"
            return ans
        def render(self):
            return f'''<table>{self.__render_table()}</table>'''

    class textarea(tag):
        def __init__(self, name=None, rows=None, cols=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('div',name, id, clas, style, accesskey, draggable, hidden)
            self.rows = rows
            self.cols = cols

        def extra_attributes(self):
            return f'''{' rows="'+self.rows+'"' if self.rows is not None else ""}{' cols="'+self.cols+'"' if self.cols is not None else ""}'''

    class template(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('template',name, id, clas, style, accesskey, draggable, hidden)

    class time(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, datetime=None, hidden=False):
            super().__init__('time',name, id, clas, style, accesskey, draggable, hidden)
            self.datetime = datetime

        def extra_attributes(self):
            return f'''{' datetime="'+self.datetime+'"' if self.datetime is not None else ""}'''

    class var(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None, hidden=False):
            super().__init__('var',name, id, clas, style, accesskey, draggable, hidden)

    class u(tag):
        def __init__(self, name=None, id=None, clas=None, style=None, accesskey=None, draggable=None):
            super().__init__('u',name, id, clas, style, accesskey, draggable)

    class video(tag):
        def __init__(self, autoplay=None, controls=None, loop=None, muted=None, preload=None, type=None, src=None):
            assert preload in ["auto","metadata",None], f'''Invalid attribute: {preload}'''
            self.autoplay = autoplay
            self.controls = controls
            self.loop = loop
            self.muted = muted
            self.preload = preload
            self.type = type
            self.src = src

        def render(self):
            return f'''<video{' src="'+self.src+'"' if self.src is not None else ""}{' type="'+self.type+'"' if self.type is not None else ""}{ 'autoplay' if self.autoplay else ""}{ 'controls' if self.controls else ""}{ 'loop' if self.loop else ""}{ 'muted' if self.muted else ""}{ 'preload' if self.preload else ""}/>'''

    class wbr(tag):
        def render(self):
            return '''<wbr>'''

    class img(tag):
        def __init__(self, src=None, height=None, width=None, alt=None, referrerpolicy=None, crossorigin=None, loading=None, sizes=None):
            assert src is not None, f'''Please provide source for Image'''
            assert referrerpolicy in ['no-referrer','no-referrer-when-downgrade','origin','origin-when-cross-origin','unsafe-url', None], f'''Invalid 'img' referrerpolicy: {referrerpolicy}'''
            assert crossorigin in ['anonymous', 'use-credentials',None], f'''Invalid crossorigin: {crossorigin}'''
            assert loading in ['lazy','eager',None], f'''Invalid loading type: {loading}'''
            self.src = src
            self.alt = alt
            self.height = height
            self.width = width
            self.referrerpolicy = referrerpolicy
            self.crossorigin = crossorigin
            self.loading = loading
            self.sizes = sizes

        def render(self):
            return f'''<img src="{self.src}"{' alt="'+self.alt+'"' if self.alt is not None else ""}{' height="'+self.height+'"' if self.height is not None else ""}{' width="'+self.width+'"' if self.width is not None else ""}{' referrerpolicy="'+self.referrerpolicy+'"' if self.referrerpolicy is not None else ""}{' loading="'+self.loading+'"' if self.loading is not None else ""}{' sizes="'+self.sizes+'"' if self.sizes is not None else ""}>'''