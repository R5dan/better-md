from .symbol import Symbol

# Check prop lists before use
# MDN Docs: https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/svg

# Animation elements
class Animate(Symbol):
    html = "animate"
    md = ""
    rst = ""

class AnimateMotion(Symbol):
    html = "animateMotion"
    md = ""
    rst = ""

class AnimateTransform(Symbol):
    html = "animateTransform"
    md = ""
    rst = ""

# Shape elements
class Circle(Symbol):
    prop_list = ["cx", "cy", "r"]
    html = "circle"
    md = ""
    rst = ""

class ClipPath(Symbol):
    html = "clipPath"
    md = ""
    rst = ""

class Cursor(Symbol):
    html = "cursor"
    md = ""
    rst = ""

class Defs(Symbol):
    html = "defs"
    md = ""
    rst = ""

class Desc(Symbol):
    html = "desc"
    md = ""
    rst = ""

class Discard(Symbol):
    html = "discard"
    md = ""
    rst = ""

class Ellipse(Symbol):
    prop_list = ["cx", "cy", "rx", "ry"]
    html = "ellipse"
    md = ""
    rst = ""

# Filter elements
class FeBlend(Symbol):
    html = "feBlend"
    md = ""
    rst = ""

class FeColorMatrix(Symbol):
    html = "feColorMatrix"
    md = ""
    rst = ""

class FeComponentTransfer(Symbol):
    html = "feComponentTransfer"
    md = ""
    rst = ""

class FeComposite(Symbol):
    html = "feComposite"
    md = ""
    rst = ""

class FeConvolveMatrix(Symbol):
    html = "feConvolveMatrix"
    md = ""
    rst = ""

class FeDiffuseLighting(Symbol):
    html = "feDiffuseLighting"
    md = ""
    rst = ""

class FeDisplacementMap(Symbol):
    html = "feDisplacementMap"
    md = ""
    rst = ""

class FeDistantLight(Symbol):
    html = "feDistantLight"
    md = ""
    rst = ""

class FeDropShadow(Symbol):
    html = "feDropShadow"
    md = ""
    rst = ""

class FeFlood(Symbol):
    html = "feFlood"
    md = ""
    rst = ""

class FeFuncA(Symbol):
    html = "feFuncA"
    md = ""
    rst = ""

class FeFuncB(Symbol):
    html = "feFuncB"
    md = ""
    rst = ""

class FeFuncG(Symbol):
    html = "feFuncG"
    md = ""
    rst = ""

class FeFuncR(Symbol):
    html = "feFuncR"
    md = ""
    rst = ""

class FeGaussianBlur(Symbol):
    html = "feGaussianBlur"
    md = ""
    rst = ""

class FeImage(Symbol):
    html = "feImage"
    md = ""
    rst = ""

class FeMerge(Symbol):
    html = "feMerge"
    md = ""
    rst = ""

class FeMergeNode(Symbol):
    html = "feMergeNode"
    md = ""
    rst = ""

class FeMorphology(Symbol):
    html = "feMorphology"
    md = ""
    rst = ""

class FeOffset(Symbol):
    html = "feOffset"
    md = ""
    rst = ""

class FePointLight(Symbol):
    html = "fePointLight"
    md = ""
    rst = ""

class FeSpecularLighting(Symbol):
    html = "feSpecularLighting"
    md = ""
    rst = ""

class FeSpotLight(Symbol):
    html = "feSpotLight"
    md = ""
    rst = ""

class FeTile(Symbol):
    html = "feTile"
    md = ""
    rst = ""

class FeTurbulence(Symbol):
    html = "feTurbulence"
    md = ""
    rst = ""

class Filter(Symbol):
    html = "filter"
    md = ""
    rst = ""

# Font elements (deprecated but included)
class FontFaceFormat(Symbol):
    html = "font-face-format"
    md = ""
    rst = ""

class FontFaceName(Symbol):
    html = "font-face-name"
    md = ""
    rst = ""

class FontFaceSrc(Symbol):
    html = "font-face-src"
    md = ""
    rst = ""

class FontFaceUri(Symbol):
    html = "font-face-uri"
    md = ""
    rst = ""

class FontFace(Symbol):
    html = "font-face"
    md = ""
    rst = ""

class Font(Symbol):
    html = "font"
    md = ""
    rst = ""

# Other SVG elements
class ForeignObject(Symbol):
    html = "foreignObject"
    md = ""
    rst = ""

class G(Symbol):
    html = "g"
    md = ""
    rst = ""

class Glyph(Symbol):
    html = "glyph"
    md = ""
    rst = ""

class GlyphRef(Symbol):
    html = "glyphRef"
    md = ""
    rst = ""

class HKern(Symbol):
    html = "hkern"
    md = ""
    rst = ""

class Image(Symbol):
    prop_list = ["href", "x", "y", "width", "height"]
    html = "image"
    md = ""
    rst = ""

class Line(Symbol):
    prop_list = ["x1", "y1", "x2", "y2"]
    html = "line"
    md = ""
    rst = ""

class LinearGradient(Symbol):
    html = "linearGradient"
    md = ""
    rst = ""

class Marker(Symbol):
    html = "marker"
    md = ""
    rst = ""

class Mask(Symbol):
    html = "mask"
    md = ""
    rst = ""

class Metadata(Symbol):
    html = "metadata"
    md = ""
    rst = ""

class MissingGlyph(Symbol):
    html = "missing-glyph"
    md = ""
    rst = ""

class MPath(Symbol):
    html = "mpath"
    md = ""
    rst = ""

class Path(Symbol):
    prop_list = ["d"]
    html = "path"
    md = ""
    rst = ""

class Pattern(Symbol):
    html = "pattern"
    md = ""
    rst = ""

class Polygon(Symbol):
    prop_list = ["points"]
    html = "polygon"
    md = ""
    rst = ""

class Polyline(Symbol):
    prop_list = ["points"]
    html = "polyline"
    md = ""
    rst = ""

class RadialGradient(Symbol):
    html = "radialGradient"
    md = ""
    rst = ""

class Rect(Symbol):
    prop_list = ["x", "y", "width", "height", "rx", "ry"]
    html = "rect"
    md = ""
    rst = ""

class SVGScript(Symbol):
    html = "script"
    md = ""
    rst = ""

class Set(Symbol):
    html = "set"
    md = ""
    rst = ""

class Stop(Symbol):
    html = "stop"
    md = ""
    rst = ""

class Style(Symbol):
    html = "style"
    md = ""
    rst = ""

class Svg(Symbol):
    prop_list = ["width", "height", "viewBox"]
    html = "svg"
    md = ""
    rst = ""

class Switch(Symbol):
    html = "switch"
    md = ""
    rst = ""

class SVGSymbol(Symbol):
    html = "symbol"
    md = ""
    rst = ""

class SVGText(Symbol):
    html = "text"
    md = ""
    rst = ""

class TextPath(Symbol):
    html = "textPath"
    md = ""
    rst = ""

class Title(Symbol):
    html = "title"
    md = ""
    rst = ""

class TRef(Symbol):
    html = "tref"
    md = ""
    rst = ""

class TSpan(Symbol):
    html = "tspan"
    md = ""
    rst = ""

class Use(Symbol):
    prop_list = ["href", "x", "y", "width", "height"]
    html = "use"
    md = ""
    rst = ""

class View(Symbol):
    html = "view"
    md = ""
    rst = ""

class VKern(Symbol):
    html = "vkern"
    md = ""
    rst = ""