import { g as ne, w as S, d as re, a as x } from "./Index-nicRoqtV.js";
const b = window.ms_globals.React, C = window.ms_globals.React.useMemo, B = window.ms_globals.React.useState, V = window.ms_globals.React.useEffect, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, P = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.ColorPicker;
var q = {
  exports: {}
}, k = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = b, le = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ie = Object.prototype.hasOwnProperty, ae = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function J(n, t, o) {
  var r, s = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t) ie.call(t, r) && !ue.hasOwnProperty(r) && (s[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) s[r] === void 0 && (s[r] = t[r]);
  return {
    $$typeof: le,
    type: n,
    key: e,
    ref: l,
    props: s,
    _owner: ae.current
  };
}
k.Fragment = ce;
k.jsx = J;
k.jsxs = J;
q.exports = k;
var y = q.exports;
const {
  SvelteComponent: de,
  assign: A,
  binding_callbacks: F,
  check_outros: fe,
  children: Y,
  claim_element: K,
  claim_space: pe,
  component_subscribe: N,
  compute_slots: _e,
  create_slot: he,
  detach: E,
  element: Q,
  empty: W,
  exclude_internal_props: D,
  get_all_dirty_from_scope: me,
  get_slot_changes: ge,
  group_outros: be,
  init: we,
  insert_hydration: I,
  safe_not_equal: ye,
  set_custom_element_data: X,
  space: Ee,
  transition_in: R,
  transition_out: j,
  update_slot_base: xe
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: Se,
  onDestroy: Ie,
  setContext: Re
} = window.__gradio__svelte__internal;
function H(n) {
  let t, o;
  const r = (
    /*#slots*/
    n[7].default
  ), s = he(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = Q("svelte-slot"), s && s.c(), this.h();
    },
    l(e) {
      t = K(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = Y(t);
      s && s.l(l), l.forEach(E), this.h();
    },
    h() {
      X(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      I(e, t, l), s && s.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      s && s.p && (!o || l & /*$$scope*/
      64) && xe(
        s,
        r,
        e,
        /*$$scope*/
        e[6],
        o ? ge(
          r,
          /*$$scope*/
          e[6],
          l,
          null
        ) : me(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (R(s, e), o = !0);
    },
    o(e) {
      j(s, e), o = !1;
    },
    d(e) {
      e && E(t), s && s.d(e), n[9](null);
    }
  };
}
function Ce(n) {
  let t, o, r, s, e = (
    /*$$slots*/
    n[4].default && H(n)
  );
  return {
    c() {
      t = Q("react-portal-target"), o = Ee(), e && e.c(), r = W(), this.h();
    },
    l(l) {
      t = K(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(t).forEach(E), o = pe(l), e && e.l(l), r = W(), this.h();
    },
    h() {
      X(t, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      I(l, t, i), n[8](t), I(l, o, i), e && e.m(l, i), I(l, r, i), s = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, i), i & /*$$slots*/
      16 && R(e, 1)) : (e = H(l), e.c(), R(e, 1), e.m(r.parentNode, r)) : e && (be(), j(e, 1, 1, () => {
        e = null;
      }), fe());
    },
    i(l) {
      s || (R(e), s = !0);
    },
    o(l) {
      j(e), s = !1;
    },
    d(l) {
      l && (E(t), E(o), E(r)), n[8](null), e && e.d(l);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function ke(n, t, o) {
  let r, s, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const i = _e(e);
  let {
    svelteInit: c
  } = t;
  const _ = S(M(t)), a = S();
  N(n, a, (d) => o(0, r = d));
  const f = S();
  N(n, f, (d) => o(1, s = d));
  const u = [], h = Se("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: m,
    subSlotIndex: g
  } = ne() || {}, w = c({
    parent: h,
    props: _,
    target: a,
    slot: f,
    slotKey: p,
    slotIndex: m,
    subSlotIndex: g,
    onDestroy(d) {
      u.push(d);
    }
  });
  Re("$$ms-gr-react-wrapper", w), ve(() => {
    _.set(M(t));
  }), Ie(() => {
    u.forEach((d) => d());
  });
  function v(d) {
    F[d ? "unshift" : "push"](() => {
      r = d, a.set(r);
    });
  }
  function $(d) {
    F[d ? "unshift" : "push"](() => {
      s = d, f.set(s);
    });
  }
  return n.$$set = (d) => {
    o(17, t = A(A({}, t), D(d))), "svelteInit" in d && o(5, c = d.svelteInit), "$$scope" in d && o(6, l = d.$$scope);
  }, t = D(t), [r, s, a, f, i, c, l, e, v, $];
}
class Oe extends de {
  constructor(t) {
    super(), we(this, t, ke, Ce, ye, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, O = window.ms_globals.tree;
function Pe(n) {
  function t(o) {
    const r = S(), s = new Oe({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? O;
          return i.nodes = [...i.nodes, l], z({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== r), z({
              createPortal: P,
              node: O
            });
          }), l;
        },
        ...o.props
      }
    });
    return r.set(s), s;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
function je(n) {
  const [t, o] = B(() => x(n));
  return V(() => {
    let r = !0;
    return n.subscribe((e) => {
      r && (r = !1, e === t) || o(e);
    });
  }, [n]), t;
}
function Te(n) {
  const t = C(() => re(n, (o) => o), [n]);
  return je(t);
}
function Le(n) {
  try {
    if (typeof n == "string") {
      let t = n.trim();
      return t.startsWith(";") && (t = t.slice(1)), t.endsWith(";") && (t = t.slice(0, -1)), new Function(`return (...args) => (${t})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function G(n) {
  return C(() => Le(n), [n]);
}
function Ae(n, t) {
  const o = C(() => b.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, l) => {
    if (e.props.node.slotIndex && l.props.node.slotIndex) {
      const i = x(e.props.node.slotIndex) || 0, c = x(l.props.node.slotIndex) || 0;
      return i - c === 0 && e.props.node.subSlotIndex && l.props.node.subSlotIndex ? (x(e.props.node.subSlotIndex) || 0) - (x(l.props.node.subSlotIndex) || 0) : i - c;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Te(o);
}
const Fe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ne(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const r = n[o];
    return typeof r == "number" && !Fe.includes(o) ? t[o] = r + "px" : t[o] = r, t;
  }, {}) : {};
}
function T(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(b.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: b.Children.toArray(n._reactElement.props.children).map((s) => {
        if (b.isValidElement(s) && s.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = T(s.props.el);
          return b.cloneElement(s, {
            ...s.props,
            el: l,
            children: [...b.Children.toArray(s.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((s) => {
    n.getEventListeners(s).forEach(({
      listener: l,
      type: i,
      useCapture: c
    }) => {
      o.addEventListener(i, l, c);
    });
  });
  const r = Array.from(n.childNodes);
  for (let s = 0; s < r.length; s++) {
    const e = r[s];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = T(e);
      t.push(...i), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function We(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const L = ee(({
  slot: n,
  clone: t,
  className: o,
  style: r
}, s) => {
  const e = te(), [l, i] = B([]);
  return V(() => {
    var f;
    if (!e.current || !n)
      return;
    let c = n;
    function _() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), We(s, u), o && u.classList.add(...o.split(" ")), r) {
        const h = Ne(r);
        Object.keys(h).forEach((p) => {
          u.style[p] = h[p];
        });
      }
    }
    let a = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var g, w, v;
        (g = e.current) != null && g.contains(c) && ((w = e.current) == null || w.removeChild(c));
        const {
          portals: p,
          clonedElement: m
        } = T(n);
        return c = m, i(p), c.style.display = "contents", _(), (v = e.current) == null || v.appendChild(c), p.length > 0;
      };
      u() || (a = new window.MutationObserver(() => {
        u() && (a == null || a.disconnect());
      }), a.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", _(), (f = e.current) == null || f.appendChild(c);
    return () => {
      var u, h;
      c.style.display = "", (u = e.current) != null && u.contains(c) && ((h = e.current) == null || h.removeChild(c)), a == null || a.disconnect();
    };
  }, [n, t, o, r, s]), b.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Z(n, t, o) {
  return n.filter(Boolean).map((r, s) => {
    var c;
    if (typeof r != "object")
      return r;
    const e = {
      ...r.props,
      key: ((c = r.props) == null ? void 0 : c.key) ?? (o ? `${o}-${s}` : `${s}`)
    };
    let l = e;
    Object.keys(r.slots).forEach((_) => {
      if (!r.slots[_] || !(r.slots[_] instanceof Element) && !r.slots[_].el)
        return;
      const a = _.split(".");
      a.forEach((m, g) => {
        l[m] || (l[m] = {}), g !== a.length - 1 && (l = e[m]);
      });
      const f = r.slots[_];
      let u, h, p = !1;
      f instanceof Element ? u = f : (u = f.el, h = f.callback, p = f.clone ?? !1), l[a[a.length - 1]] = u ? h ? (...m) => (h(a[a.length - 1], m), /* @__PURE__ */ y.jsx(L, {
        slot: u,
        clone: p
      })) : /* @__PURE__ */ y.jsx(L, {
        slot: u,
        clone: p
      }) : l[a[a.length - 1]], l = e;
    });
    const i = "children";
    return r[i] && (e[i] = Z(r[i], t, `${s}`)), e;
  });
}
function De(n, t) {
  return n ? /* @__PURE__ */ y.jsx(L, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function U({
  key: n,
  setSlotParams: t,
  slots: o
}, r) {
  return o[n] ? (...s) => (t(n, s), De(o[n], {
    clone: !0,
    ...r
  })) : void 0;
}
const Me = Pe(({
  onValueChange: n,
  onChange: t,
  panelRender: o,
  showText: r,
  value: s,
  presets: e,
  presetItems: l,
  children: i,
  value_format: c,
  setSlotParams: _,
  slots: a,
  ...f
}) => {
  const u = G(o), h = G(r), p = Ae(i);
  return /* @__PURE__ */ y.jsxs(y.Fragment, {
    children: [p.length === 0 && /* @__PURE__ */ y.jsx("div", {
      style: {
        display: "none"
      },
      children: i
    }), /* @__PURE__ */ y.jsx(oe, {
      ...f,
      value: s,
      presets: C(() => e || Z(l), [e, l]),
      showText: a.showText ? U({
        slots: a,
        setSlotParams: _,
        key: "showText"
      }) : h || r,
      panelRender: a.panelRender ? U({
        slots: a,
        setSlotParams: _,
        key: "panelRender"
      }) : u,
      onChange: (m, ...g) => {
        const w = {
          rgb: m.toRgbString(),
          hex: m.toHexString(),
          hsb: m.toHsbString()
        };
        t == null || t(w[c], ...g), n(w[c]);
      },
      children: p.length === 0 ? null : i
    })]
  });
});
export {
  Me as ColorPicker,
  Me as default
};
