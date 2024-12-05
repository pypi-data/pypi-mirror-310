import { g as X, w as E } from "./Index-CZ_jkiac.js";
const m = window.ms_globals.React, q = window.ms_globals.React.useMemo, V = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.QRCode;
var D = {
  exports: {}
}, C = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var $ = m, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(n, e, o) {
  var s, r = {}, t = null, l = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) ne.call(e, s) && !oe.hasOwnProperty(s) && (r[s] = e[s]);
  if (n && n.defaultProps) for (s in e = n.defaultProps, e) r[s] === void 0 && (r[s] = e[s]);
  return {
    $$typeof: ee,
    type: n,
    key: t,
    ref: l,
    props: r,
    _owner: re.current
  };
}
C.Fragment = te;
C.jsx = M;
C.jsxs = M;
D.exports = C;
var z = D.exports;
const {
  SvelteComponent: se,
  assign: k,
  binding_callbacks: L,
  check_outros: le,
  children: G,
  claim_element: U,
  claim_space: ie,
  component_subscribe: T,
  compute_slots: ce,
  create_slot: ae,
  detach: h,
  element: H,
  empty: N,
  exclude_internal_props: j,
  get_all_dirty_from_scope: ue,
  get_slot_changes: de,
  group_outros: fe,
  init: _e,
  insert_hydration: v,
  safe_not_equal: pe,
  set_custom_element_data: K,
  space: me,
  transition_in: R,
  transition_out: O,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function A(n) {
  let e, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = ae(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = H("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      e = U(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = G(e);
      r && r.l(l), l.forEach(h), this.h();
    },
    h() {
      K(e, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      v(t, e, l), r && r.m(e, null), n[9](e), o = !0;
    },
    p(t, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && he(
        r,
        s,
        t,
        /*$$scope*/
        t[6],
        o ? de(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : ue(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (R(r, t), o = !0);
    },
    o(t) {
      O(r, t), o = !1;
    },
    d(t) {
      t && h(e), r && r.d(t), n[9](null);
    }
  };
}
function Ee(n) {
  let e, o, s, r, t = (
    /*$$slots*/
    n[4].default && A(n)
  );
  return {
    c() {
      e = H("react-portal-target"), o = me(), t && t.c(), s = N(), this.h();
    },
    l(l) {
      e = U(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(e).forEach(h), o = ie(l), t && t.l(l), s = N(), this.h();
    },
    h() {
      K(e, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      v(l, e, c), n[8](e), v(l, o, c), t && t.m(l, c), v(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, c), c & /*$$slots*/
      16 && R(t, 1)) : (t = A(l), t.c(), R(t, 1), t.m(s.parentNode, s)) : t && (fe(), O(t, 1, 1, () => {
        t = null;
      }), le());
    },
    i(l) {
      r || (R(t), r = !0);
    },
    o(l) {
      O(t), r = !1;
    },
    d(l) {
      l && (h(e), h(o), h(s)), n[8](null), t && t.d(l);
    }
  };
}
function F(n) {
  const {
    svelteInit: e,
    ...o
  } = n;
  return o;
}
function ve(n, e, o) {
  let s, r, {
    $$slots: t = {},
    $$scope: l
  } = e;
  const c = ce(t);
  let {
    svelteInit: i
  } = e;
  const g = E(F(e)), d = E();
  T(n, d, (a) => o(0, s = a));
  const p = E();
  T(n, p, (a) => o(1, r = a));
  const u = [], f = we("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: S,
    subSlotIndex: w
  } = X() || {}, b = i({
    parent: f,
    props: g,
    target: d,
    slot: p,
    slotKey: _,
    slotIndex: S,
    subSlotIndex: w,
    onDestroy(a) {
      u.push(a);
    }
  });
  ye("$$ms-gr-react-wrapper", b), ge(() => {
    g.set(F(e));
  }), be(() => {
    u.forEach((a) => a());
  });
  function y(a) {
    L[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function Q(a) {
    L[a ? "unshift" : "push"](() => {
      r = a, p.set(r);
    });
  }
  return n.$$set = (a) => {
    o(17, e = k(k({}, e), j(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, e = j(e), [s, r, d, p, c, i, l, t, y, Q];
}
class Re extends se {
  constructor(e) {
    super(), _e(this, e, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, x = window.ms_globals.tree;
function Ce(n) {
  function e(o) {
    const s = E(), r = new Re({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? x;
          return c.nodes = [...c.nodes, l], W({
            createPortal: I,
            node: x
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), W({
              createPortal: I,
              node: x
            });
          }), l;
        },
        ...o.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(e);
    });
  });
}
function Se(n) {
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
function xe(n) {
  return q(() => Se(n), [n]);
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(n) {
  return n ? Object.keys(n).reduce((e, o) => {
    const s = n[o];
    return typeof s == "number" && !Ie.includes(o) ? e[o] = s + "px" : e[o] = s, e;
  }, {}) : {};
}
function P(n) {
  const e = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(I(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = P(r.props.el);
          return m.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...m.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const t = s[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = P(t);
      e.push(...c), o.appendChild(l);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function Pe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const ke = V(({
  slot: n,
  clone: e,
  className: o,
  style: s
}, r) => {
  const t = B(), [l, c] = J([]);
  return Y(() => {
    var p;
    if (!t.current || !n)
      return;
    let i = n;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Pe(r, u), o && u.classList.add(...o.split(" ")), s) {
        const f = Oe(s);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let u = function() {
        var w, b, y;
        (w = t.current) != null && w.contains(i) && ((b = t.current) == null || b.removeChild(i));
        const {
          portals: _,
          clonedElement: S
        } = P(n);
        return i = S, c(_), i.style.display = "contents", g(), (y = t.current) == null || y.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (p = t.current) == null || p.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((f = t.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, e, o, s, r]), m.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Le(n, e) {
  return n ? /* @__PURE__ */ z.jsx(ke, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Te({
  key: n,
  setSlotParams: e,
  slots: o
}, s) {
  return o[n] ? (...r) => (e(n, r), Le(o[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const je = Ce(({
  setSlotParams: n,
  slots: e,
  statusRender: o,
  ...s
}) => {
  const r = xe(o);
  return /* @__PURE__ */ z.jsx(Z, {
    ...s,
    statusRender: e.statusRender ? Te({
      slots: e,
      setSlotParams: n,
      key: "statusRender"
    }) : r
  });
});
export {
  je as QRCode,
  je as default
};
