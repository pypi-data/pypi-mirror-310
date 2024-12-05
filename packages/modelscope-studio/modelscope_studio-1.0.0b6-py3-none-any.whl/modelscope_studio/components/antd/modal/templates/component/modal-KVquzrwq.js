import { g as ee, w as C } from "./Index-hT7mF2fd.js";
const w = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, $ = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Modal;
var G = {
  exports: {}
}, P = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = w, oe = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(e, t, r) {
  var l, o = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) le.call(t, l) && !ce.hasOwnProperty(l) && (o[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: oe,
    type: e,
    key: n,
    ref: s,
    props: o,
    _owner: se.current
  };
}
P.Fragment = re;
P.jsx = U;
P.jsxs = U;
G.exports = P;
var m = G.exports;
const {
  SvelteComponent: ie,
  assign: L,
  binding_callbacks: B,
  check_outros: ae,
  children: H,
  claim_element: K,
  claim_space: ue,
  component_subscribe: F,
  compute_slots: de,
  create_slot: fe,
  detach: b,
  element: q,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: _e,
  get_slot_changes: me,
  group_outros: pe,
  init: he,
  insert_hydration: I,
  safe_not_equal: ge,
  set_custom_element_data: V,
  space: we,
  transition_in: R,
  transition_out: T,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ee,
  onDestroy: xe,
  setContext: ve
} = window.__gradio__svelte__internal;
function M(e) {
  let t, r;
  const l = (
    /*#slots*/
    e[7].default
  ), o = fe(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = q("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = K(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(t);
      o && o.l(s), s.forEach(b), this.h();
    },
    h() {
      V(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      I(n, t, s), o && o.m(t, null), e[9](t), r = !0;
    },
    p(n, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && be(
        o,
        l,
        n,
        /*$$scope*/
        n[6],
        r ? me(
          l,
          /*$$scope*/
          n[6],
          s,
          null
        ) : _e(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (R(o, n), r = !0);
    },
    o(n) {
      T(o, n), r = !1;
    },
    d(n) {
      n && b(t), o && o.d(n), e[9](null);
    }
  };
}
function Ce(e) {
  let t, r, l, o, n = (
    /*$$slots*/
    e[4].default && M(e)
  );
  return {
    c() {
      t = q("react-portal-target"), r = we(), n && n.c(), l = N(), this.h();
    },
    l(s) {
      t = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(b), r = ue(s), n && n.l(s), l = N(), this.h();
    },
    h() {
      V(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      I(s, t, c), e[8](t), I(s, r, c), n && n.m(s, c), I(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, c), c & /*$$slots*/
      16 && R(n, 1)) : (n = M(s), n.c(), R(n, 1), n.m(l.parentNode, l)) : n && (pe(), T(n, 1, 1, () => {
        n = null;
      }), ae());
    },
    i(s) {
      o || (R(n), o = !0);
    },
    o(s) {
      T(n), o = !1;
    },
    d(s) {
      s && (b(t), b(r), b(l)), e[8](null), n && n.d(s);
    }
  };
}
function W(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Ie(e, t, r) {
  let l, o, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const c = de(n);
  let {
    svelteInit: i
  } = t;
  const g = C(W(t)), d = C();
  F(e, d, (u) => r(0, l = u));
  const _ = C();
  F(e, _, (u) => r(1, o = u));
  const a = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: k,
    subSlotIndex: y
  } = ee() || {}, E = i({
    parent: f,
    props: g,
    target: d,
    slot: _,
    slotKey: p,
    slotIndex: k,
    subSlotIndex: y,
    onDestroy(u) {
      a.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", E), ye(() => {
    g.set(W(t));
  }), xe(() => {
    a.forEach((u) => u());
  });
  function x(u) {
    B[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function J(u) {
    B[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return e.$$set = (u) => {
    r(17, t = L(L({}, t), A(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, t = A(t), [l, o, d, _, c, i, s, n, x, J];
}
class Re extends ie {
  constructor(t) {
    super(), he(this, t, Ie, Ce, ge, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, S = window.ms_globals.tree;
function Pe(e) {
  function t(r) {
    const l = C(), o = new Re({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? S;
          return c.nodes = [...c.nodes, s], D({
            createPortal: O,
            node: S
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: O,
              node: S
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const l = e[r];
    return typeof l == "number" && !ke.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function j(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(O(w.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: w.Children.toArray(e._reactElement.props.children).map((o) => {
        if (w.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = j(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...w.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const n = l[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = j(n);
      t.push(...c), r.appendChild(s);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Oe(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const h = Y(({
  slot: e,
  clone: t,
  className: r,
  style: l
}, o) => {
  const n = Q(), [s, c] = X([]);
  return Z(() => {
    var _;
    if (!n.current || !e)
      return;
    let i = e;
    function g() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(o, a), r && a.classList.add(...r.split(" ")), l) {
        const f = Se(l);
        Object.keys(f).forEach((p) => {
          a.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var y, E, x;
        (y = n.current) != null && y.contains(i) && ((E = n.current) == null || E.removeChild(i));
        const {
          portals: p,
          clonedElement: k
        } = j(e);
        return i = k, c(p), i.style.display = "contents", g(), (x = n.current) == null || x.appendChild(i), p.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (_ = n.current) == null || _.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = n.current) != null && a.contains(i) && ((f = n.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, t, r, l, o]), w.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Te(e) {
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
function v(e) {
  return $(() => Te(e), [e]);
}
function je(e, t) {
  return e ? /* @__PURE__ */ m.jsx(h, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function z({
  key: e,
  setSlotParams: t,
  slots: r
}, l) {
  return r[e] ? (...o) => (t(e, o), je(r[e], {
    clone: !0,
    ...l
  })) : void 0;
}
const Be = Pe(({
  slots: e,
  afterClose: t,
  afterOpenChange: r,
  getContainer: l,
  children: o,
  modalRender: n,
  setSlotParams: s,
  ...c
}) => {
  var a, f;
  const i = v(r), g = v(t), d = v(l), _ = v(n);
  return /* @__PURE__ */ m.jsx(te, {
    ...c,
    afterOpenChange: i,
    afterClose: g,
    okText: e.okText ? /* @__PURE__ */ m.jsx(h, {
      slot: e.okText
    }) : c.okText,
    okButtonProps: {
      ...c.okButtonProps || {},
      icon: e["okButtonProps.icon"] ? /* @__PURE__ */ m.jsx(h, {
        slot: e["okButtonProps.icon"]
      }) : (a = c.okButtonProps) == null ? void 0 : a.icon
    },
    cancelText: e.cancelText ? /* @__PURE__ */ m.jsx(h, {
      slot: e.cancelText
    }) : c.cancelText,
    cancelButtonProps: {
      ...c.cancelButtonProps || {},
      icon: e["cancelButtonProps.icon"] ? /* @__PURE__ */ m.jsx(h, {
        slot: e["cancelButtonProps.icon"]
      }) : (f = c.cancelButtonProps) == null ? void 0 : f.icon
    },
    closable: e["closable.closeIcon"] ? {
      ...typeof c.closable == "object" ? c.closable : {},
      closeIcon: /* @__PURE__ */ m.jsx(h, {
        slot: e["closable.closeIcon"]
      })
    } : c.closable,
    closeIcon: e.closeIcon ? /* @__PURE__ */ m.jsx(h, {
      slot: e.closeIcon
    }) : c.closeIcon,
    footer: e.footer ? z({
      slots: e,
      setSlotParams: s,
      key: "footer"
    }) : c.footer,
    title: e.title ? /* @__PURE__ */ m.jsx(h, {
      slot: e.title
    }) : c.title,
    modalRender: e.modalRender ? z({
      slots: e,
      setSlotParams: s,
      key: "modalRender"
    }) : _,
    getContainer: typeof l == "string" ? d : l,
    children: o
  });
});
export {
  Be as Modal,
  Be as default
};
