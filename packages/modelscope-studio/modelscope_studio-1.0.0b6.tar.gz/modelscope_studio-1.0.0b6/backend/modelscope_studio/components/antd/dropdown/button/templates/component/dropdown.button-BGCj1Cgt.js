import { g as ne, w as R, d as re, a as v } from "./Index-kUwhCTVC.js";
const w = window.ms_globals.React, k = window.ms_globals.React.useMemo, H = window.ms_globals.React.useState, V = window.ms_globals.React.useEffect, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, T = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.Dropdown;
var q = {
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
var se = w, le = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ae = Object.prototype.hasOwnProperty, ie = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function J(n, e, o) {
  var r, l = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (r in e) ae.call(e, r) && !ue.hasOwnProperty(r) && (l[r] = e[r]);
  if (n && n.defaultProps) for (r in e = n.defaultProps, e) l[r] === void 0 && (l[r] = e[r]);
  return {
    $$typeof: le,
    type: n,
    key: t,
    ref: s,
    props: l,
    _owner: ie.current
  };
}
O.Fragment = ce;
O.jsx = J;
O.jsxs = J;
q.exports = O;
var E = q.exports;
const {
  SvelteComponent: de,
  assign: F,
  binding_callbacks: N,
  check_outros: fe,
  children: Y,
  claim_element: K,
  claim_space: pe,
  component_subscribe: D,
  compute_slots: _e,
  create_slot: me,
  detach: y,
  element: Q,
  empty: W,
  exclude_internal_props: B,
  get_all_dirty_from_scope: he,
  get_slot_changes: ge,
  group_outros: we,
  init: be,
  insert_hydration: C,
  safe_not_equal: ye,
  set_custom_element_data: X,
  space: Ee,
  transition_in: S,
  transition_out: L,
  update_slot_base: ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ie,
  getContext: xe,
  onDestroy: Re,
  setContext: Ce
} = window.__gradio__svelte__internal;
function M(n) {
  let e, o;
  const r = (
    /*#slots*/
    n[7].default
  ), l = me(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = Q("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = K(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(e);
      l && l.l(s), s.forEach(y), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      C(t, e, s), l && l.m(e, null), n[9](e), o = !0;
    },
    p(t, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && ve(
        l,
        r,
        t,
        /*$$scope*/
        t[6],
        o ? ge(
          r,
          /*$$scope*/
          t[6],
          s,
          null
        ) : he(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (S(l, t), o = !0);
    },
    o(t) {
      L(l, t), o = !1;
    },
    d(t) {
      t && y(e), l && l.d(t), n[9](null);
    }
  };
}
function Se(n) {
  let e, o, r, l, t = (
    /*$$slots*/
    n[4].default && M(n)
  );
  return {
    c() {
      e = Q("react-portal-target"), o = Ee(), t && t.c(), r = W(), this.h();
    },
    l(s) {
      e = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(e).forEach(y), o = pe(s), t && t.l(s), r = W(), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      C(s, e, c), n[8](e), C(s, o, c), t && t.m(s, c), C(s, r, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && S(t, 1)) : (t = M(s), t.c(), S(t, 1), t.m(r.parentNode, r)) : t && (we(), L(t, 1, 1, () => {
        t = null;
      }), fe());
    },
    i(s) {
      l || (S(t), l = !0);
    },
    o(s) {
      L(t), l = !1;
    },
    d(s) {
      s && (y(e), y(o), y(r)), n[8](null), t && t.d(s);
    }
  };
}
function z(n) {
  const {
    svelteInit: e,
    ...o
  } = n;
  return o;
}
function ke(n, e, o) {
  let r, l, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const c = _e(t);
  let {
    svelteInit: a
  } = e;
  const h = R(z(e)), u = R();
  D(n, u, (d) => o(0, r = d));
  const f = R();
  D(n, f, (d) => o(1, l = d));
  const i = [], p = xe("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: m,
    subSlotIndex: g
  } = ne() || {}, b = a({
    parent: p,
    props: h,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: m,
    subSlotIndex: g,
    onDestroy(d) {
      i.push(d);
    }
  });
  Ce("$$ms-gr-react-wrapper", b), Ie(() => {
    h.set(z(e));
  }), Re(() => {
    i.forEach((d) => d());
  });
  function x(d) {
    N[d ? "unshift" : "push"](() => {
      r = d, u.set(r);
    });
  }
  function $(d) {
    N[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  return n.$$set = (d) => {
    o(17, e = F(F({}, e), B(d))), "svelteInit" in d && o(5, a = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, e = B(e), [r, l, u, f, c, a, s, t, x, $];
}
class Oe extends de {
  constructor(e) {
    super(), be(this, e, ke, Se, ye, {
      svelteInit: 5
    });
  }
}
const G = window.ms_globals.rerender, P = window.ms_globals.tree;
function Pe(n) {
  function e(o) {
    const r = R(), l = new Oe({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? P;
          return c.nodes = [...c.nodes, s], G({
            createPortal: T,
            node: P
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((a) => a.svelteInstance !== r), G({
              createPortal: T,
              node: P
            });
          }), s;
        },
        ...o.props
      }
    });
    return r.set(l), l;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(e);
    });
  });
}
function je(n) {
  const [e, o] = H(() => v(n));
  return V(() => {
    let r = !0;
    return n.subscribe((t) => {
      r && (r = !1, t === e) || o(t);
    });
  }, [n]), e;
}
function Te(n) {
  const e = k(() => re(n, (o) => o), [n]);
  return je(e);
}
const Le = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(n) {
  return n ? Object.keys(n).reduce((e, o) => {
    const r = n[o];
    return typeof r == "number" && !Le.includes(o) ? e[o] = r + "px" : e[o] = r, e;
  }, {}) : {};
}
function A(n) {
  const e = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(T(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((l) => {
        if (w.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = A(l.props.el);
          return w.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...w.Children.toArray(l.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: s,
      type: c,
      useCapture: a
    }) => {
      o.addEventListener(c, s, a);
    });
  });
  const r = Array.from(n.childNodes);
  for (let l = 0; l < r.length; l++) {
    const t = r[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = A(t);
      e.push(...c), o.appendChild(s);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function Fe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const I = ee(({
  slot: n,
  clone: e,
  className: o,
  style: r
}, l) => {
  const t = te(), [s, c] = H([]);
  return V(() => {
    var f;
    if (!t.current || !n)
      return;
    let a = n;
    function h() {
      let i = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (i = a.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Fe(l, i), o && i.classList.add(...o.split(" ")), r) {
        const p = Ae(r);
        Object.keys(p).forEach((_) => {
          i.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let i = function() {
        var g, b, x;
        (g = t.current) != null && g.contains(a) && ((b = t.current) == null || b.removeChild(a));
        const {
          portals: _,
          clonedElement: m
        } = A(n);
        return a = m, c(_), a.style.display = "contents", h(), (x = t.current) == null || x.appendChild(a), _.length > 0;
      };
      i() || (u = new window.MutationObserver(() => {
        i() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      a.style.display = "contents", h(), (f = t.current) == null || f.appendChild(a);
    return () => {
      var i, p;
      a.style.display = "", (i = t.current) != null && i.contains(a) && ((p = t.current) == null || p.removeChild(a)), u == null || u.disconnect();
    };
  }, [n, e, o, r, l]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ne(n) {
  try {
    if (typeof n == "string") {
      let e = n.trim();
      return e.startsWith(";") && (e = e.slice(1)), e.endsWith(";") && (e = e.slice(0, -1)), new Function(`return (...args) => (${e})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function j(n) {
  return k(() => Ne(n), [n]);
}
function De(n, e) {
  const o = k(() => w.Children.toArray(n).filter((t) => t.props.node && e === t.props.nodeSlotKey).sort((t, s) => {
    if (t.props.node.slotIndex && s.props.node.slotIndex) {
      const c = v(t.props.node.slotIndex) || 0, a = v(s.props.node.slotIndex) || 0;
      return c - a === 0 && t.props.node.subSlotIndex && s.props.node.subSlotIndex ? (v(t.props.node.subSlotIndex) || 0) - (v(s.props.node.subSlotIndex) || 0) : c - a;
    }
    return 0;
  }).map((t) => t.props.node.target), [n, e]);
  return Te(o);
}
function Z(n, e, o) {
  return n.filter(Boolean).map((r, l) => {
    var a;
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const t = {
      ...r.props,
      key: ((a = r.props) == null ? void 0 : a.key) ?? (o ? `${o}-${l}` : `${l}`)
    };
    let s = t;
    Object.keys(r.slots).forEach((h) => {
      if (!r.slots[h] || !(r.slots[h] instanceof Element) && !r.slots[h].el)
        return;
      const u = h.split(".");
      u.forEach((m, g) => {
        s[m] || (s[m] = {}), g !== u.length - 1 && (s = t[m]);
      });
      const f = r.slots[h];
      let i, p, _ = (e == null ? void 0 : e.clone) ?? !1;
      f instanceof Element ? i = f : (i = f.el, p = f.callback, _ = f.clone ?? !1), s[u[u.length - 1]] = i ? p ? (...m) => (p(u[u.length - 1], m), /* @__PURE__ */ E.jsx(I, {
        slot: i,
        clone: _
      })) : /* @__PURE__ */ E.jsx(I, {
        slot: i,
        clone: _
      }) : s[u[u.length - 1]], s = t;
    });
    const c = (e == null ? void 0 : e.children) || "children";
    return r[c] && (t[c] = Z(r[c], e, `${l}`)), t;
  });
}
function We(n, e) {
  return n ? /* @__PURE__ */ E.jsx(I, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function U({
  key: n,
  setSlotParams: e,
  slots: o
}, r) {
  return o[n] ? (...l) => (e(n, l), We(o[n], {
    clone: !0,
    ...r
  })) : void 0;
}
const Me = Pe(({
  getPopupContainer: n,
  slots: e,
  menuItems: o,
  children: r,
  dropdownRender: l,
  buttonsRender: t,
  setSlotParams: s,
  ...c
}) => {
  var i, p, _;
  const a = j(n), h = j(l), u = j(t), f = De(r, "buttonsRender");
  return /* @__PURE__ */ E.jsx(oe.Button, {
    ...c,
    buttonsRender: f.length ? (...m) => (s("buttonsRender", m), f.map((g, b) => /* @__PURE__ */ E.jsx(I, {
      slot: g
    }, b))) : u,
    menu: {
      ...c.menu,
      items: k(() => {
        var m;
        return ((m = c.menu) == null ? void 0 : m.items) || Z(o, {
          clone: !0
        });
      }, [o, (i = c.menu) == null ? void 0 : i.items]),
      expandIcon: e["menu.expandIcon"] ? U({
        slots: e,
        setSlotParams: s,
        key: "menu.expandIcon"
      }, {
        clone: !0
      }) : (p = c.menu) == null ? void 0 : p.expandIcon,
      overflowedIndicator: e["menu.overflowedIndicator"] ? /* @__PURE__ */ E.jsx(I, {
        slot: e["menu.overflowedIndicator"]
      }) : (_ = c.menu) == null ? void 0 : _.overflowedIndicator
    },
    getPopupContainer: a,
    dropdownRender: e.dropdownRender ? U({
      slots: e,
      setSlotParams: s,
      key: "dropdownRender"
    }) : h,
    children: r
  });
});
export {
  Me as DropdownButton,
  Me as default
};
