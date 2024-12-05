import { g as $, w as x } from "./Index-DpDIBnka.js";
const m = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Drawer;
var G = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = m, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, le = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(t, n, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) oe.call(n, l) && !se.hasOwnProperty(l) && (r[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) r[l] === void 0 && (r[l] = n[l]);
  return {
    $$typeof: ne,
    type: t,
    key: e,
    ref: s,
    props: r,
    _owner: le.current
  };
}
I.Fragment = re;
I.jsx = U;
I.jsxs = U;
G.exports = I;
var h = G.exports;
const {
  SvelteComponent: ie,
  assign: T,
  binding_callbacks: F,
  check_outros: ce,
  children: H,
  claim_element: K,
  claim_space: ae,
  component_subscribe: N,
  compute_slots: ue,
  create_slot: de,
  detach: g,
  element: q,
  empty: A,
  exclude_internal_props: D,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: C,
  safe_not_equal: he,
  set_custom_element_data: V,
  space: ge,
  transition_in: R,
  transition_out: j,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function W(t) {
  let n, o;
  const l = (
    /*#slots*/
    t[7].default
  ), r = de(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = q("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      n = K(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(n);
      r && r.l(s), s.forEach(g), this.h();
    },
    h() {
      V(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      C(e, n, s), r && r.m(n, null), t[9](n), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && we(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? _e(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : fe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (R(r, e), o = !0);
    },
    o(e) {
      j(r, e), o = !1;
    },
    d(e) {
      e && g(n), r && r.d(e), t[9](null);
    }
  };
}
function xe(t) {
  let n, o, l, r, e = (
    /*$$slots*/
    t[4].default && W(t)
  );
  return {
    c() {
      n = q("react-portal-target"), o = ge(), e && e.c(), l = A(), this.h();
    },
    l(s) {
      n = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(n).forEach(g), o = ae(s), e && e.l(s), l = A(), this.h();
    },
    h() {
      V(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      C(s, n, c), t[8](n), C(s, o, c), e && e.m(s, c), C(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && R(e, 1)) : (e = W(s), e.c(), R(e, 1), e.m(l.parentNode, l)) : e && (pe(), j(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      r || (R(e), r = !0);
    },
    o(s) {
      j(e), r = !1;
    },
    d(s) {
      s && (g(n), g(o), g(l)), t[8](null), e && e.d(s);
    }
  };
}
function M(t) {
  const {
    svelteInit: n,
    ...o
  } = t;
  return o;
}
function Ce(t, n, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const c = ue(e);
  let {
    svelteInit: i
  } = n;
  const w = x(M(n)), d = x();
  N(t, d, (a) => o(0, l = a));
  const p = x();
  N(t, p, (a) => o(1, r = a));
  const u = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: S,
    subSlotIndex: y
  } = $() || {}, E = i({
    parent: f,
    props: w,
    target: d,
    slot: p,
    slotKey: _,
    slotIndex: S,
    subSlotIndex: y,
    onDestroy(a) {
      u.push(a);
    }
  });
  ve("$$ms-gr-react-wrapper", E), be(() => {
    w.set(M(n));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function v(a) {
    F[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function B(a) {
    F[a ? "unshift" : "push"](() => {
      r = a, p.set(r);
    });
  }
  return t.$$set = (a) => {
    o(17, n = T(T({}, n), D(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, n = D(n), [l, r, d, p, c, i, s, e, v, B];
}
class Re extends ie {
  constructor(n) {
    super(), me(this, n, Ce, xe, he, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ie(t) {
  function n(o) {
    const l = x(), r = new Re({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? O;
          return c.nodes = [...c.nodes, s], z({
            createPortal: k,
            node: O
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), z({
              createPortal: k,
              node: O
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(t) {
  return t ? Object.keys(t).reduce((n, o) => {
    const l = t[o];
    return typeof l == "number" && !Se.includes(o) ? n[o] = l + "px" : n[o] = l, n;
  }, {}) : {};
}
function L(t) {
  const n = [], o = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(k(m.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: m.Children.toArray(t._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = L(r.props.el);
          return m.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...m.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, s, i);
    });
  });
  const l = Array.from(t.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = L(e);
      n.push(...c), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Pe(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const b = J(({
  slot: t,
  clone: n,
  className: o,
  style: l
}, r) => {
  const e = Y(), [s, c] = Q([]);
  return X(() => {
    var p;
    if (!e.current || !t)
      return;
    let i = t;
    function w() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Pe(r, u), o && u.classList.add(...o.split(" ")), l) {
        const f = Oe(l);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var y, E, v;
        (y = e.current) != null && y.contains(i) && ((E = e.current) == null || E.removeChild(i));
        const {
          portals: _,
          clonedElement: S
        } = L(t);
        return i = S, c(_), i.style.display = "contents", w(), (v = e.current) == null || v.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, n, o, l, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function ke(t) {
  try {
    if (typeof t == "string") {
      let n = t.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function P(t) {
  return Z(() => ke(t), [t]);
}
function je(t, n) {
  return t ? /* @__PURE__ */ h.jsx(b, {
    slot: t,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Le({
  key: t,
  setSlotParams: n,
  slots: o
}, l) {
  return o[t] ? (...r) => (n(t, r), je(o[t], {
    clone: !0,
    ...l
  })) : void 0;
}
const Fe = Ie(({
  slots: t,
  afterOpenChange: n,
  getContainer: o,
  drawerRender: l,
  setSlotParams: r,
  ...e
}) => {
  const s = P(n), c = P(o), i = P(l);
  return /* @__PURE__ */ h.jsx(ee, {
    ...e,
    afterOpenChange: s,
    closeIcon: t.closeIcon ? /* @__PURE__ */ h.jsx(b, {
      slot: t.closeIcon
    }) : e.closeIcon,
    extra: t.extra ? /* @__PURE__ */ h.jsx(b, {
      slot: t.extra
    }) : e.extra,
    footer: t.footer ? /* @__PURE__ */ h.jsx(b, {
      slot: t.footer
    }) : e.footer,
    title: t.title ? /* @__PURE__ */ h.jsx(b, {
      slot: t.title
    }) : e.title,
    drawerRender: t.drawerRender ? Le({
      slots: t,
      setSlotParams: r,
      key: "drawerRender"
    }) : i,
    getContainer: typeof o == "string" ? c : o
  });
});
export {
  Fe as Drawer,
  Fe as default
};
