package fyi.gildas.callrecorder

import android.graphics.drawable.ColorDrawable
import android.graphics.drawable.Drawable
import android.graphics.drawable.GradientDrawable
import android.graphics.drawable.RippleDrawable
import android.view.View
import android.view.ViewGroup
import android.widget.CompoundButton
import android.widget.EditText
import android.widget.ImageView
import android.widget.TextView
import org.json.JSONArray
import org.json.JSONObject

/** Le relevé d'un écran : chaque vue visible, sa place en dp, son texte, ses couleurs, ce qu'elle dit à l'accessibilité. */
object Releve {
    private fun hex(c: Int) = String.format("#%08X", c)

    private fun fill(d: Drawable?): JSONObject? = when (d) {
        null -> null
        is GradientDrawable -> JSONObject().put("kind", "gradient").put("color", d.color?.defaultColor?.let { hex(it) }).put("radius", d.cornerRadius.toDouble()).put("shape", d.shape)
        is RippleDrawable -> JSONObject().put("kind", "ripple").put("layer", if (d.numberOfLayers > 0) fill(d.getDrawable(0)) else null)
        is ColorDrawable -> JSONObject().put("kind", "color").put("color", hex(d.color))
        else -> JSONObject().put("kind", d.javaClass.simpleName)
    }

    fun dump(v: View, parent: Int, ox: Int, oy: Int, density: Float, fontScale: Float, out: JSONArray) {
        if (v.visibility != View.VISIBLE) return
        val x = ox + v.left - (if (parent >= 0) 0 else v.left)
        val y = oy + v.top - (if (parent >= 0) 0 else v.top)
        val o = JSONObject()
        val me = out.length()
        o.put("i", me).put("parent", parent).put("cls", v.javaClass.simpleName)
            .put("x", x / density).put("y", y / density).put("w", v.width / density).put("h", v.height / density)
            .put("alpha", v.alpha.toDouble()).put("elevation", v.elevation / density)
            .put("clickable", v.isClickable).put("focusable", v.isFocusable)
            .put("important", v.importantForAccessibility).put("heading", v.isAccessibilityHeading)
            .put("minH", v.minimumHeight / density).put("minW", v.minimumWidth / density)
            .put("pad", JSONArray().put(v.paddingLeft / density).put(v.paddingTop / density).put(v.paddingRight / density).put(v.paddingBottom / density))
        v.contentDescription?.let { o.put("desc", it.toString()) }
        v.stateDescription?.let { o.put("state", it.toString()) }
        fill(v.background)?.let { o.put("bg", it) }
        if (v is TextView) {
            o.put("text", v.text.toString()).put("sp", v.textSize / density / fontScale).put("px", v.textSize.toDouble())
                .put("color", hex(v.currentTextColor)).put("weight", v.typeface?.weight ?: 400).put("bold", v.typeface?.isBold ?: false)
                .put("lineMult", v.lineSpacingMultiplier.toDouble()).put("lineExtra", v.lineSpacingExtra / density)
                .put("lineHeight", v.lineHeight / density).put("maxLines", v.maxLines).put("lines", v.layout?.lineCount ?: -1)
                .put("ellipsized", (0 until (v.layout?.lineCount ?: 0)).any { v.layout.getEllipsisCount(it) > 0 })
                .put("gravity", v.gravity).put("features", v.fontFeatureSettings ?: "")
            if (v is EditText) o.put("hint", v.hint?.toString() ?: "").put("hintColor", hex(v.currentHintTextColor))
            if (v is CompoundButton) o.put("checked", v.isChecked)
        }
        if (v is ImageView) { (v.tag as? Int)?.let { o.put("res", v.resources.getResourceEntryName(it)) } }
        out.put(o)
        if (v is ViewGroup) for (k in 0 until v.childCount) {
            val c = v.getChildAt(k)
            // ListView : les enfants sont à leur place dans la liste.
            dump(c, me, x - v.scrollX, y - v.scrollY, density, fontScale, out)
        }
    }
}
