import { g as Z, w as C } from "./Index-gDIrNxxM.js";
const p = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.Alert;
var z = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ee = p, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, re = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, t, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) oe.call(t, s) && !se.hasOwnProperty(s) && (r[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: te,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: re.current
  };
}
R.Fragment = ne;
R.jsx = G;
R.jsxs = G;
z.exports = R;
var h = z.exports;
const {
  SvelteComponent: le,
  assign: L,
  binding_callbacks: A,
  check_outros: ie,
  children: U,
  claim_element: H,
  claim_space: ce,
  component_subscribe: T,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: K,
  empty: N,
  exclude_internal_props: F,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: me,
  insert_hydration: x,
  safe_not_equal: pe,
  set_custom_element_data: q,
  space: he,
  transition_in: I,
  transition_out: k,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function W(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = ue(
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
      r && r.l(l), l.forEach(g), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      x(e, t, l), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && ge(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? fe(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (I(r, e), o = !0);
    },
    o(e) {
      k(r, e), o = !1;
    },
    d(e) {
      e && g(t), r && r.d(e), n[9](null);
    }
  };
}
function ve(n) {
  let t, o, s, r, e = (
    /*$$slots*/
    n[4].default && W(n)
  );
  return {
    c() {
      t = K("react-portal-target"), o = he(), e && e.c(), s = N(), this.h();
    },
    l(l) {
      t = H(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(g), o = ce(l), e && e.l(l), s = N(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      x(l, t, c), n[8](t), x(l, o, c), e && e.m(l, c), x(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && I(e, 1)) : (e = W(l), e.c(), I(e, 1), e.m(s.parentNode, s)) : e && (_e(), k(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(l) {
      r || (I(e), r = !0);
    },
    o(l) {
      k(e), r = !1;
    },
    d(l) {
      l && (g(t), g(o), g(s)), n[8](null), e && e.d(l);
    }
  };
}
function D(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Ce(n, t, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = ae(e);
  let {
    svelteInit: i
  } = t;
  const w = C(D(t)), d = C();
  T(n, d, (a) => o(0, s = a));
  const m = C();
  T(n, m, (a) => o(1, r = a));
  const u = [], f = be("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: S,
    subSlotIndex: y
  } = Z() || {}, E = i({
    parent: f,
    props: w,
    target: d,
    slot: m,
    slotKey: _,
    slotIndex: S,
    subSlotIndex: y,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", E), we(() => {
    w.set(D(t));
  }), ye(() => {
    u.forEach((a) => a());
  });
  function v(a) {
    A[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function V(a) {
    A[a ? "unshift" : "push"](() => {
      r = a, m.set(r);
    });
  }
  return n.$$set = (a) => {
    o(17, t = L(L({}, t), F(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, t = F(t), [s, r, d, m, c, i, l, e, v, V];
}
class xe extends le {
  constructor(t) {
    super(), me(this, t, Ce, ve, pe, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ie(n) {
  function t(o) {
    const s = C(), r = new xe({
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
          }, c = e.parent ?? O;
          return c.nodes = [...c.nodes, l], M({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), M({
              createPortal: P,
              node: O
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
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !Re.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function j(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(p.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: p.Children.toArray(n._reactElement.props.children).map((r) => {
        if (p.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = j(r.props.el);
          return p.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...p.Children.toArray(r.props.children), ...e]
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
      } = j(e);
      t.push(...c), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Oe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const b = B(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, r) => {
  const e = J(), [l, c] = Y([]);
  return Q(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function w() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Oe(r, u), o && u.classList.add(...o.split(" ")), s) {
        const f = Se(s);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var y, E, v;
        (y = e.current) != null && y.contains(i) && ((E = e.current) == null || E.removeChild(i));
        const {
          portals: _,
          clonedElement: S
        } = j(n);
        return i = S, c(_), i.style.display = "contents", w(), (v = e.current) == null || v.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, o, s, r]), p.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Pe(n) {
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
function ke(n) {
  return X(() => Pe(n), [n]);
}
const Le = Ie(({
  slots: n,
  afterClose: t,
  ...o
}) => {
  const s = ke(t);
  return /* @__PURE__ */ h.jsx($, {
    ...o,
    afterClose: s,
    action: n.action ? /* @__PURE__ */ h.jsx(b, {
      slot: n.action
    }) : o.action,
    closable: n["closable.closeIcon"] ? {
      ...typeof o.closable == "object" ? o.closable : {},
      closeIcon: /* @__PURE__ */ h.jsx(b, {
        slot: n["closable.closeIcon"]
      })
    } : o.closable,
    description: n.description ? /* @__PURE__ */ h.jsx(b, {
      slot: n.description
    }) : o.description,
    icon: n.icon ? /* @__PURE__ */ h.jsx(b, {
      slot: n.icon
    }) : o.icon,
    message: n.message ? /* @__PURE__ */ h.jsx(b, {
      slot: n.message
    }) : o.message
  });
});
export {
  Le as Alert,
  Le as default
};
