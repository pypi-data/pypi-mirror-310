import { g as le, w as C } from "./Index-CAatmXZ-.js";
const E = window.ms_globals.React, te = window.ms_globals.React.forwardRef, ne = window.ms_globals.React.useRef, re = window.ms_globals.React.useState, oe = window.ms_globals.React.useEffect, q = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, se = window.ms_globals.antd.Select;
var B = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ce = E, ae = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), de = Object.prototype.hasOwnProperty, ue = ce.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, fe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, t, s) {
  var r, o = {}, n = null, l = null;
  s !== void 0 && (n = "" + s), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t) de.call(t, r) && !fe.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: ae,
    type: e,
    key: n,
    ref: l,
    props: o,
    _owner: ue.current
  };
}
O.Fragment = ie;
O.jsx = V;
O.jsxs = V;
B.exports = O;
var g = B.exports;
const {
  SvelteComponent: _e,
  assign: A,
  binding_callbacks: W,
  check_outros: me,
  children: J,
  claim_element: Y,
  claim_space: he,
  component_subscribe: D,
  compute_slots: pe,
  create_slot: ge,
  detach: v,
  element: K,
  empty: M,
  exclude_internal_props: z,
  get_all_dirty_from_scope: we,
  get_slot_changes: be,
  group_outros: ye,
  init: Ee,
  insert_hydration: S,
  safe_not_equal: Ie,
  set_custom_element_data: Q,
  space: Re,
  transition_in: k,
  transition_out: T,
  update_slot_base: ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: Ce,
  onDestroy: Se,
  setContext: ke
} = window.__gradio__svelte__internal;
function G(e) {
  let t, s;
  const r = (
    /*#slots*/
    e[7].default
  ), o = ge(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = Y(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = J(t);
      o && o.l(l), l.forEach(v), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      S(n, t, l), o && o.m(t, null), e[9](t), s = !0;
    },
    p(n, l) {
      o && o.p && (!s || l & /*$$scope*/
      64) && ve(
        o,
        r,
        n,
        /*$$scope*/
        n[6],
        s ? be(
          r,
          /*$$scope*/
          n[6],
          l,
          null
        ) : we(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      s || (k(o, n), s = !0);
    },
    o(n) {
      T(o, n), s = !1;
    },
    d(n) {
      n && v(t), o && o.d(n), e[9](null);
    }
  };
}
function Oe(e) {
  let t, s, r, o, n = (
    /*$$slots*/
    e[4].default && G(e)
  );
  return {
    c() {
      t = K("react-portal-target"), s = Re(), n && n.c(), r = M(), this.h();
    },
    l(l) {
      t = Y(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(t).forEach(v), s = he(l), n && n.l(l), r = M(), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      S(l, t, a), e[8](t), S(l, s, a), n && n.m(l, a), S(l, r, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, a), a & /*$$slots*/
      16 && k(n, 1)) : (n = G(l), n.c(), k(n, 1), n.m(r.parentNode, r)) : n && (ye(), T(n, 1, 1, () => {
        n = null;
      }), me());
    },
    i(l) {
      o || (k(n), o = !0);
    },
    o(l) {
      T(n), o = !1;
    },
    d(l) {
      l && (v(t), v(s), v(r)), e[8](null), n && n.d(l);
    }
  };
}
function U(e) {
  const {
    svelteInit: t,
    ...s
  } = e;
  return s;
}
function Pe(e, t, s) {
  let r, o, {
    $$slots: n = {},
    $$scope: l
  } = t;
  const a = pe(n);
  let {
    svelteInit: c
  } = t;
  const p = C(U(t)), d = C();
  D(e, d, (u) => s(0, r = u));
  const m = C();
  D(e, m, (u) => s(1, o = u));
  const i = [], h = Ce("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: _,
    subSlotIndex: w
  } = le() || {}, I = c({
    parent: h,
    props: p,
    target: d,
    slot: m,
    slotKey: f,
    slotIndex: _,
    subSlotIndex: w,
    onDestroy(u) {
      i.push(u);
    }
  });
  ke("$$ms-gr-react-wrapper", I), xe(() => {
    p.set(U(t));
  }), Se(() => {
    i.forEach((u) => u());
  });
  function R(u) {
    W[u ? "unshift" : "push"](() => {
      r = u, d.set(r);
    });
  }
  function P(u) {
    W[u ? "unshift" : "push"](() => {
      o = u, m.set(o);
    });
  }
  return e.$$set = (u) => {
    s(17, t = A(A({}, t), z(u))), "svelteInit" in u && s(5, c = u.svelteInit), "$$scope" in u && s(6, l = u.$$scope);
  }, t = z(t), [r, o, d, m, a, c, l, n, R, P];
}
class je extends _e {
  constructor(t) {
    super(), Ee(this, t, Pe, Oe, Ie, {
      svelteInit: 5
    });
  }
}
const H = window.ms_globals.rerender, j = window.ms_globals.tree;
function Fe(e) {
  function t(s) {
    const r = C(), o = new je({
      ...s,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, a = n.parent ?? j;
          return a.nodes = [...a.nodes, l], H({
            createPortal: F,
            node: j
          }), n.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== r), H({
              createPortal: F,
              node: j
            });
          }), l;
        },
        ...s.props
      }
    });
    return r.set(o), o;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(t);
    });
  });
}
const Te = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Le(e) {
  return e ? Object.keys(e).reduce((t, s) => {
    const r = e[s];
    return typeof r == "number" && !Te.includes(s) ? t[s] = r + "px" : t[s] = r, t;
  }, {}) : {};
}
function L(e) {
  const t = [], s = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(F(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((o) => {
        if (E.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: l
          } = L(o.props.el);
          return E.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...E.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: l,
      type: a,
      useCapture: c
    }) => {
      s.addEventListener(a, l, c);
    });
  });
  const r = Array.from(e.childNodes);
  for (let o = 0; o < r.length; o++) {
    const n = r[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = L(n);
      t.push(...a), s.appendChild(l);
    } else n.nodeType === 3 && s.appendChild(n.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function Ne(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const b = te(({
  slot: e,
  clone: t,
  className: s,
  style: r
}, o) => {
  const n = ne(), [l, a] = re([]);
  return oe(() => {
    var m;
    if (!n.current || !e)
      return;
    let c = e;
    function p() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Ne(o, i), s && i.classList.add(...s.split(" ")), r) {
        const h = Le(r);
        Object.keys(h).forEach((f) => {
          i.style[f] = h[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var w, I, R;
        (w = n.current) != null && w.contains(c) && ((I = n.current) == null || I.removeChild(c));
        const {
          portals: f,
          clonedElement: _
        } = L(e);
        return c = _, a(f), c.style.display = "contents", p(), (R = n.current) == null || R.appendChild(c), f.length > 0;
      };
      i() || (d = new window.MutationObserver(() => {
        i() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", p(), (m = n.current) == null || m.appendChild(c);
    return () => {
      var i, h;
      c.style.display = "", (i = n.current) != null && i.contains(c) && ((h = n.current) == null || h.removeChild(c)), d == null || d.disconnect();
    };
  }, [e, t, s, r, o]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ae(e) {
  try {
    if (typeof e == "string") {
      let t = e.trim();
      return t.startsWith(";") && (t = t.slice(1)), t.endsWith(";") && (t = t.slice(0, -1)), new Function(`return (...args) => (${t})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function y(e) {
  return q(() => Ae(e), [e]);
}
function X(e, t, s) {
  return e.filter(Boolean).map((r, o) => {
    var c;
    if (typeof r != "object")
      return t != null && t.fallback ? t.fallback(r) : r;
    const n = {
      ...r.props,
      key: ((c = r.props) == null ? void 0 : c.key) ?? (s ? `${s}-${o}` : `${o}`)
    };
    let l = n;
    Object.keys(r.slots).forEach((p) => {
      if (!r.slots[p] || !(r.slots[p] instanceof Element) && !r.slots[p].el)
        return;
      const d = p.split(".");
      d.forEach((_, w) => {
        l[_] || (l[_] = {}), w !== d.length - 1 && (l = n[_]);
      });
      const m = r.slots[p];
      let i, h, f = (t == null ? void 0 : t.clone) ?? !1;
      m instanceof Element ? i = m : (i = m.el, h = m.callback, f = m.clone ?? !1), l[d[d.length - 1]] = i ? h ? (..._) => (h(d[d.length - 1], _), /* @__PURE__ */ g.jsx(b, {
        slot: i,
        clone: f
      })) : /* @__PURE__ */ g.jsx(b, {
        slot: i,
        clone: f
      }) : l[d[d.length - 1]], l = n;
    });
    const a = (t == null ? void 0 : t.children) || "children";
    return r[a] && (n[a] = X(r[a], t, `${o}`)), n;
  });
}
function We(e, t) {
  return e ? /* @__PURE__ */ g.jsx(b, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function x({
  key: e,
  setSlotParams: t,
  slots: s
}, r) {
  return s[e] ? (...o) => (t(e, o), We(s[e], {
    clone: !0,
    ...r
  })) : void 0;
}
const Me = Fe(({
  slots: e,
  children: t,
  onValueChange: s,
  filterOption: r,
  onChange: o,
  options: n,
  optionItems: l,
  getPopupContainer: a,
  dropdownRender: c,
  optionRender: p,
  tagRender: d,
  labelRender: m,
  filterSort: i,
  elRef: h,
  setSlotParams: f,
  ..._
}) => {
  const w = y(a), I = y(r), R = y(c), P = y(i), u = y(p), Z = y(d), $ = y(m);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ g.jsx(se, {
      ..._,
      ref: h,
      options: q(() => n || X(l, {
        children: "options",
        clone: !0
      }), [l, n]),
      onChange: (N, ...ee) => {
        o == null || o(N, ...ee), s(N);
      },
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ g.jsx(b, {
          slot: e["allowClear.clearIcon"]
        })
      } : _.allowClear,
      removeIcon: e.removeIcon ? /* @__PURE__ */ g.jsx(b, {
        slot: e.removeIcon
      }) : _.removeIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ g.jsx(b, {
        slot: e.suffixIcon
      }) : _.suffixIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ g.jsx(b, {
        slot: e.notFoundContent
      }) : _.notFoundContent,
      menuItemSelectedIcon: e.menuItemSelectedIcon ? /* @__PURE__ */ g.jsx(b, {
        slot: e.menuItemSelectedIcon
      }) : _.menuItemSelectedIcon,
      filterOption: I || r,
      maxTagPlaceholder: e.maxTagPlaceholder ? x({
        slots: e,
        setSlotParams: f,
        key: "maxTagPlaceholder"
      }) : _.maxTagPlaceholder,
      getPopupContainer: w,
      dropdownRender: e.dropdownRender ? x({
        slots: e,
        setSlotParams: f,
        key: "dropdownRender"
      }) : R,
      optionRender: e.optionRender ? x({
        slots: e,
        setSlotParams: f,
        key: "optionRender"
      }) : u,
      tagRender: e.tagRender ? x({
        slots: e,
        setSlotParams: f,
        key: "tagRender"
      }) : Z,
      labelRender: e.labelRender ? x({
        slots: e,
        setSlotParams: f,
        key: "labelRender"
      }) : $,
      filterSort: P
    })]
  });
});
export {
  Me as Select,
  Me as default
};
