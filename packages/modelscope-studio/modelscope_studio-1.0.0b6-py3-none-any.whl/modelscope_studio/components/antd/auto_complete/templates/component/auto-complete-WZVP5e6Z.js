import { b as ee, g as te, w as x } from "./Index-CTDZFUxy.js";
const C = window.ms_globals.React, U = window.ms_globals.React.forwardRef, P = window.ms_globals.React.useRef, H = window.ms_globals.React.useState, j = window.ms_globals.React.useEffect, T = window.ms_globals.React.useMemo, A = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.internalContext.AutoCompleteContext, re = window.ms_globals.antd.AutoComplete;
function le(t, e) {
  return ee(t, e);
}
var B = {
  exports: {}
}, S = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var oe = C, se = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ae = Object.prototype.hasOwnProperty, ie = oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function J(t, e, l) {
  var r, o = {}, n = null, s = null;
  l !== void 0 && (n = "" + l), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (r in e) ae.call(e, r) && !ue.hasOwnProperty(r) && (o[r] = e[r]);
  if (t && t.defaultProps) for (r in e = t.defaultProps, e) o[r] === void 0 && (o[r] = e[r]);
  return {
    $$typeof: se,
    type: t,
    key: n,
    ref: s,
    props: o,
    _owner: ie.current
  };
}
S.Fragment = ce;
S.jsx = J;
S.jsxs = J;
B.exports = S;
var m = B.exports;
const {
  SvelteComponent: de,
  assign: N,
  binding_callbacks: W,
  check_outros: fe,
  children: Y,
  claim_element: K,
  claim_space: _e,
  component_subscribe: V,
  compute_slots: pe,
  create_slot: he,
  detach: y,
  element: Q,
  empty: D,
  exclude_internal_props: M,
  get_all_dirty_from_scope: me,
  get_slot_changes: ge,
  group_outros: we,
  init: be,
  insert_hydration: R,
  safe_not_equal: Ce,
  set_custom_element_data: X,
  space: Ee,
  transition_in: I,
  transition_out: F,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: xe,
  onDestroy: Re,
  setContext: Ie
} = window.__gradio__svelte__internal;
function q(t) {
  let e, l;
  const r = (
    /*#slots*/
    t[7].default
  ), o = he(
    r,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = Q("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      e = K(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(e);
      o && o.l(s), s.forEach(y), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      R(n, e, s), o && o.m(e, null), t[9](e), l = !0;
    },
    p(n, s) {
      o && o.p && (!l || s & /*$$scope*/
      64) && ye(
        o,
        r,
        n,
        /*$$scope*/
        n[6],
        l ? ge(
          r,
          /*$$scope*/
          n[6],
          s,
          null
        ) : me(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      l || (I(o, n), l = !0);
    },
    o(n) {
      F(o, n), l = !1;
    },
    d(n) {
      n && y(e), o && o.d(n), t[9](null);
    }
  };
}
function Se(t) {
  let e, l, r, o, n = (
    /*$$slots*/
    t[4].default && q(t)
  );
  return {
    c() {
      e = Q("react-portal-target"), l = Ee(), n && n.c(), r = D(), this.h();
    },
    l(s) {
      e = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(e).forEach(y), l = _e(s), n && n.l(s), r = D(), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      R(s, e, a), t[8](e), R(s, l, a), n && n.m(s, a), R(s, r, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, a), a & /*$$slots*/
      16 && I(n, 1)) : (n = q(s), n.c(), I(n, 1), n.m(r.parentNode, r)) : n && (we(), F(n, 1, 1, () => {
        n = null;
      }), fe());
    },
    i(s) {
      o || (I(n), o = !0);
    },
    o(s) {
      F(n), o = !1;
    },
    d(s) {
      s && (y(e), y(l), y(r)), t[8](null), n && n.d(s);
    }
  };
}
function z(t) {
  const {
    svelteInit: e,
    ...l
  } = t;
  return l;
}
function Oe(t, e, l) {
  let r, o, {
    $$slots: n = {},
    $$scope: s
  } = e;
  const a = pe(n);
  let {
    svelteInit: c
  } = e;
  const h = x(z(e)), u = x();
  V(t, u, (d) => l(0, r = d));
  const f = x();
  V(t, f, (d) => l(1, o = d));
  const i = [], _ = xe("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: g,
    subSlotIndex: w
  } = te() || {}, b = c({
    parent: _,
    props: h,
    target: u,
    slot: f,
    slotKey: p,
    slotIndex: g,
    subSlotIndex: w,
    onDestroy(d) {
      i.push(d);
    }
  });
  Ie("$$ms-gr-react-wrapper", b), ve(() => {
    h.set(z(e));
  }), Re(() => {
    i.forEach((d) => d());
  });
  function E(d) {
    W[d ? "unshift" : "push"](() => {
      r = d, u.set(r);
    });
  }
  function $(d) {
    W[d ? "unshift" : "push"](() => {
      o = d, f.set(o);
    });
  }
  return t.$$set = (d) => {
    l(17, e = N(N({}, e), M(d))), "svelteInit" in d && l(5, c = d.svelteInit), "$$scope" in d && l(6, s = d.$$scope);
  }, e = M(e), [r, o, u, f, a, c, s, n, E, $];
}
class ke extends de {
  constructor(e) {
    super(), be(this, e, Oe, Se, Ce, {
      svelteInit: 5
    });
  }
}
const G = window.ms_globals.rerender, O = window.ms_globals.tree;
function Pe(t) {
  function e(l) {
    const r = x(), o = new ke({
      ...l,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, a = n.parent ?? O;
          return a.nodes = [...a.nodes, s], G({
            createPortal: A,
            node: O
          }), n.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== r), G({
              createPortal: A,
              node: O
            });
          }), s;
        },
        ...l.props
      }
    });
    return r.set(o), o;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(e);
    });
  });
}
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(t) {
  return t ? Object.keys(t).reduce((e, l) => {
    const r = t[l];
    return typeof r == "number" && !je.includes(l) ? e[l] = r + "px" : e[l] = r, e;
  }, {}) : {};
}
function L(t) {
  const e = [], l = t.cloneNode(!1);
  if (t._reactElement)
    return e.push(A(C.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: C.Children.toArray(t._reactElement.props.children).map((o) => {
        if (C.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = L(o.props.el);
          return C.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...C.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), l)), {
      clonedElement: l,
      portals: e
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      l.addEventListener(a, s, c);
    });
  });
  const r = Array.from(t.childNodes);
  for (let o = 0; o < r.length; o++) {
    const n = r[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = L(n);
      e.push(...a), l.appendChild(s);
    } else n.nodeType === 3 && l.appendChild(n.cloneNode());
  }
  return {
    clonedElement: l,
    portals: e
  };
}
function Fe(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const v = U(({
  slot: t,
  clone: e,
  className: l,
  style: r
}, o) => {
  const n = P(), [s, a] = H([]);
  return j(() => {
    var f;
    if (!n.current || !t)
      return;
    let c = t;
    function h() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Fe(o, i), l && i.classList.add(...l.split(" ")), r) {
        const _ = Ae(r);
        Object.keys(_).forEach((p) => {
          i.style[p] = _[p];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let i = function() {
        var w, b, E;
        (w = n.current) != null && w.contains(c) && ((b = n.current) == null || b.removeChild(c));
        const {
          portals: p,
          clonedElement: g
        } = L(t);
        return c = g, a(p), c.style.display = "contents", h(), (E = n.current) == null || E.appendChild(c), p.length > 0;
      };
      i() || (u = new window.MutationObserver(() => {
        i() && (u == null || u.disconnect());
      }), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", h(), (f = n.current) == null || f.appendChild(c);
    return () => {
      var i, _;
      c.style.display = "", (i = n.current) != null && i.contains(c) && ((_ = n.current) == null || _.removeChild(c)), u == null || u.disconnect();
    };
  }, [t, e, l, r, o]), C.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(t) {
  try {
    if (typeof t == "string") {
      let e = t.trim();
      return e.startsWith(";") && (e = e.slice(1)), e.endsWith(";") && (e = e.slice(0, -1)), new Function(`return (...args) => (${e})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function k(t) {
  return T(() => Le(t), [t]);
}
function Te({
  value: t,
  onValueChange: e
}) {
  const [l, r] = H(t), o = P(e);
  o.current = e;
  const n = P(l);
  return n.current = l, j(() => {
    o.current(l);
  }, [l]), j(() => {
    le(t, n.current) || r(t);
  }, [t]), [l, r];
}
function Z(t, e, l) {
  return t.filter(Boolean).map((r, o) => {
    var c;
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const n = {
      ...r.props,
      key: ((c = r.props) == null ? void 0 : c.key) ?? (l ? `${l}-${o}` : `${o}`)
    };
    let s = n;
    Object.keys(r.slots).forEach((h) => {
      if (!r.slots[h] || !(r.slots[h] instanceof Element) && !r.slots[h].el)
        return;
      const u = h.split(".");
      u.forEach((g, w) => {
        s[g] || (s[g] = {}), w !== u.length - 1 && (s = n[g]);
      });
      const f = r.slots[h];
      let i, _, p = (e == null ? void 0 : e.clone) ?? !1;
      f instanceof Element ? i = f : (i = f.el, _ = f.callback, p = f.clone ?? !1), s[u[u.length - 1]] = i ? _ ? (...g) => (_(u[u.length - 1], g), /* @__PURE__ */ m.jsx(v, {
        slot: i,
        clone: p
      })) : /* @__PURE__ */ m.jsx(v, {
        slot: i,
        clone: p
      }) : s[u[u.length - 1]], s = n;
    });
    const a = (e == null ? void 0 : e.children) || "children";
    return r[a] && (n[a] = Z(r[a], e, `${o}`)), n;
  });
}
function Ne(t, e) {
  return t ? /* @__PURE__ */ m.jsx(v, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function We({
  key: t,
  setSlotParams: e,
  slots: l
}, r) {
  return l[t] ? (...o) => (e(t, o), Ne(l[t], {
    clone: !0,
    ...r
  })) : void 0;
}
const Ve = U(({
  children: t,
  ...e
}, l) => /* @__PURE__ */ m.jsx(ne.Provider, {
  value: T(() => ({
    ...e,
    elRef: l
  }), [e, l]),
  children: t
})), Me = Pe(({
  slots: t,
  children: e,
  onValueChange: l,
  filterOption: r,
  onChange: o,
  options: n,
  optionItems: s,
  getPopupContainer: a,
  dropdownRender: c,
  elRef: h,
  setSlotParams: u,
  ...f
}) => {
  const i = k(a), _ = k(r), p = k(c), [g, w] = Te({
    onValueChange: l,
    value: f.value
  });
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [t.children ? null : /* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ m.jsx(re, {
      ...f,
      value: g,
      ref: h,
      allowClear: t["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(v, {
          slot: t["allowClear.clearIcon"]
        })
      } : f.allowClear,
      options: T(() => n || Z(s, {
        children: "options",
        clone: !0
      }), [s, n]),
      onChange: (b, ...E) => {
        o == null || o(b, ...E), w(b);
      },
      notFoundContent: t.notFoundContent ? /* @__PURE__ */ m.jsx(v, {
        slot: t.notFoundContent
      }) : f.notFoundContent,
      filterOption: _ || r,
      getPopupContainer: i,
      dropdownRender: t.dropdownRender ? We({
        slots: t,
        setSlotParams: u,
        key: "dropdownRender"
      }, {
        clone: !0
      }) : p,
      children: t.children ? /* @__PURE__ */ m.jsxs(Ve, {
        children: [/* @__PURE__ */ m.jsx("div", {
          style: {
            display: "none"
          },
          children: e
        }), /* @__PURE__ */ m.jsx(v, {
          slot: t.children
        })]
      }) : null
    })]
  });
});
export {
  Me as AutoComplete,
  Me as default
};
