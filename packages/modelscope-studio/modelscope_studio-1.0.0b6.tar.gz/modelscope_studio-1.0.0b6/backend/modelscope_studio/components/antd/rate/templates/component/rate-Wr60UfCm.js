import { g as Q, w as v } from "./Index-DUhVwxKQ.js";
const m = window.ms_globals.React, V = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, O = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Rate;
var z = {
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
var Z = m, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, ne = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, t, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) te.call(t, s) && !re.hasOwnProperty(s) && (r[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: $,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: ne.current
  };
}
S.Fragment = ee;
S.jsx = G;
S.jsxs = G;
z.exports = S;
var w = z.exports;
const {
  SvelteComponent: oe,
  assign: L,
  binding_callbacks: T,
  check_outros: se,
  children: U,
  claim_element: H,
  claim_space: le,
  component_subscribe: j,
  compute_slots: ie,
  create_slot: ce,
  detach: h,
  element: K,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: ae,
  get_slot_changes: de,
  group_outros: ue,
  init: fe,
  insert_hydration: R,
  safe_not_equal: _e,
  set_custom_element_data: M,
  space: pe,
  transition_in: C,
  transition_out: P,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: he,
  getContext: ge,
  onDestroy: we,
  setContext: be
} = window.__gradio__svelte__internal;
function D(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = ce(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = U(t);
      r && r.l(l), l.forEach(h), this.h();
    },
    h() {
      M(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      R(e, t, l), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && me(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? de(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : ae(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (C(r, e), o = !0);
    },
    o(e) {
      P(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function ye(n) {
  let t, o, s, r, e = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      t = K("react-portal-target"), o = pe(), e && e.c(), s = N(), this.h();
    },
    l(l) {
      t = H(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(h), o = le(l), e && e.l(l), s = N(), this.h();
    },
    h() {
      M(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      R(l, t, c), n[8](t), R(l, o, c), e && e.m(l, c), R(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = D(l), e.c(), C(e, 1), e.m(s.parentNode, s)) : e && (ue(), P(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(l) {
      r || (C(e), r = !0);
    },
    o(l) {
      P(e), r = !1;
    },
    d(l) {
      l && (h(t), h(o), h(s)), n[8](null), e && e.d(l);
    }
  };
}
function F(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Ee(n, t, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = ie(e);
  let {
    svelteInit: i
  } = t;
  const g = v(F(t)), u = v();
  j(n, u, (a) => o(0, s = a));
  const p = v();
  j(n, p, (a) => o(1, r = a));
  const d = [], f = ge("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: x,
    subSlotIndex: b
  } = Q() || {}, y = i({
    parent: f,
    props: g,
    target: u,
    slot: p,
    slotKey: _,
    slotIndex: x,
    subSlotIndex: b,
    onDestroy(a) {
      d.push(a);
    }
  });
  be("$$ms-gr-react-wrapper", y), he(() => {
    g.set(F(t));
  }), we(() => {
    d.forEach((a) => a());
  });
  function E(a) {
    T[a ? "unshift" : "push"](() => {
      s = a, u.set(s);
    });
  }
  function q(a) {
    T[a ? "unshift" : "push"](() => {
      r = a, p.set(r);
    });
  }
  return n.$$set = (a) => {
    o(17, t = L(L({}, t), A(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, t = A(t), [s, r, u, p, c, i, l, e, E, q];
}
class ve extends oe {
  constructor(t) {
    super(), fe(this, t, Ee, ye, _e, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, I = window.ms_globals.tree;
function Re(n) {
  function t(o) {
    const s = v(), r = new ve({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? I;
          return c.nodes = [...c.nodes, l], W({
            createPortal: O,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), W({
              createPortal: O,
              node: I
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
      o(t);
    });
  });
}
const Ce = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !Ce.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function k(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(O(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = k(r.props.el);
          return m.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...m.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
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
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = k(e);
      t.push(...c), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function xe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Ie = V(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, r) => {
  const e = B(), [l, c] = J([]);
  return Y(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), xe(r, d), o && d.classList.add(...o.split(" ")), s) {
        const f = Se(s);
        Object.keys(f).forEach((_) => {
          d.style[_] = f[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var b, y, E;
        (b = e.current) != null && b.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: x
        } = k(n);
        return i = x, c(_), i.style.display = "contents", g(), (E = e.current) == null || E.appendChild(i), _.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var d, f;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, t, o, s, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Oe(n, t) {
  return n ? /* @__PURE__ */ w.jsx(Ie, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Pe({
  key: n,
  setSlotParams: t,
  slots: o
}, s) {
  return o[n] ? (...r) => (t(n, r), Oe(o[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const Le = Re(({
  slots: n,
  children: t,
  onValueChange: o,
  character: s,
  onChange: r,
  setSlotParams: e,
  elRef: l,
  ...c
}) => /* @__PURE__ */ w.jsxs(w.Fragment, {
  children: [/* @__PURE__ */ w.jsx("div", {
    style: {
      display: "none"
    },
    children: t
  }), /* @__PURE__ */ w.jsx(X, {
    ...c,
    ref: l,
    onChange: (i) => {
      r == null || r(i), o(i);
    },
    character: n.character ? Pe({
      slots: n,
      setSlotParams: e,
      key: "character"
    }) : s
  })]
}));
export {
  Le as Rate,
  Le as default
};
