import { b as ee, g as te, w as C } from "./Index-WUi4P4Z8.js";
const b = window.ms_globals.React, $ = window.ms_globals.React.forwardRef, O = window.ms_globals.React.useRef, G = window.ms_globals.React.useState, P = window.ms_globals.React.useEffect, U = window.ms_globals.React.useMemo, j = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.antd.Mentions;
function re(n, e) {
  return ee(n, e);
}
var H = {
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
var le = b, oe = Symbol.for("react.element"), se = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ie = le.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function B(n, e, o) {
  var r, l = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (r in e) ce.call(e, r) && !ae.hasOwnProperty(r) && (l[r] = e[r]);
  if (n && n.defaultProps) for (r in e = n.defaultProps, e) l[r] === void 0 && (l[r] = e[r]);
  return {
    $$typeof: oe,
    type: n,
    key: t,
    ref: s,
    props: l,
    _owner: ie.current
  };
}
S.Fragment = se;
S.jsx = B;
S.jsxs = B;
H.exports = S;
var w = H.exports;
const {
  SvelteComponent: ue,
  assign: N,
  binding_callbacks: A,
  check_outros: de,
  children: J,
  claim_element: Y,
  claim_space: fe,
  component_subscribe: M,
  compute_slots: _e,
  create_slot: pe,
  detach: y,
  element: K,
  empty: V,
  exclude_internal_props: W,
  get_all_dirty_from_scope: he,
  get_slot_changes: me,
  group_outros: ge,
  init: be,
  insert_hydration: R,
  safe_not_equal: we,
  set_custom_element_data: Q,
  space: Ee,
  transition_in: x,
  transition_out: F,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: Ce,
  onDestroy: Re,
  setContext: xe
} = window.__gradio__svelte__internal;
function D(n) {
  let e, o;
  const r = (
    /*#slots*/
    n[7].default
  ), l = pe(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = K("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = Y(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = J(e);
      l && l.l(s), s.forEach(y), this.h();
    },
    h() {
      Q(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      R(t, e, s), l && l.m(e, null), n[9](e), o = !0;
    },
    p(t, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && ye(
        l,
        r,
        t,
        /*$$scope*/
        t[6],
        o ? me(
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
      o || (x(l, t), o = !0);
    },
    o(t) {
      F(l, t), o = !1;
    },
    d(t) {
      t && y(e), l && l.d(t), n[9](null);
    }
  };
}
function Se(n) {
  let e, o, r, l, t = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      e = K("react-portal-target"), o = Ee(), t && t.c(), r = V(), this.h();
    },
    l(s) {
      e = Y(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(e).forEach(y), o = fe(s), t && t.l(s), r = V(), this.h();
    },
    h() {
      Q(e, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      R(s, e, i), n[8](e), R(s, o, i), t && t.m(s, i), R(s, r, i), l = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, i), i & /*$$slots*/
      16 && x(t, 1)) : (t = D(s), t.c(), x(t, 1), t.m(r.parentNode, r)) : t && (ge(), F(t, 1, 1, () => {
        t = null;
      }), de());
    },
    i(s) {
      l || (x(t), l = !0);
    },
    o(s) {
      F(t), l = !1;
    },
    d(s) {
      s && (y(e), y(o), y(r)), n[8](null), t && t.d(s);
    }
  };
}
function q(n) {
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
  const i = _e(t);
  let {
    svelteInit: c
  } = e;
  const h = C(q(e)), a = C();
  M(n, a, (d) => o(0, r = d));
  const f = C();
  M(n, f, (d) => o(1, l = d));
  const u = [], _ = Ce("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: m,
    subSlotIndex: g
  } = te() || {}, E = c({
    parent: _,
    props: h,
    target: a,
    slot: f,
    slotKey: p,
    slotIndex: m,
    subSlotIndex: g,
    onDestroy(d) {
      u.push(d);
    }
  });
  xe("$$ms-gr-react-wrapper", E), ve(() => {
    h.set(q(e));
  }), Re(() => {
    u.forEach((d) => d());
  });
  function v(d) {
    A[d ? "unshift" : "push"](() => {
      r = d, a.set(r);
    });
  }
  function Z(d) {
    A[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  return n.$$set = (d) => {
    o(17, e = N(N({}, e), W(d))), "svelteInit" in d && o(5, c = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, e = W(e), [r, l, a, f, i, c, s, t, v, Z];
}
class Ie extends ue {
  constructor(e) {
    super(), be(this, e, ke, Se, we, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, k = window.ms_globals.tree;
function Oe(n) {
  function e(o) {
    const r = C(), l = new Ie({
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
          }, i = t.parent ?? k;
          return i.nodes = [...i.nodes, s], z({
            createPortal: j,
            node: k
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== r), z({
              createPortal: j,
              node: k
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
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((e, o) => {
    const r = n[o];
    return typeof r == "number" && !Pe.includes(o) ? e[o] = r + "px" : e[o] = r, e;
  }, {}) : {};
}
function L(n) {
  const e = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(j(b.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: b.Children.toArray(n._reactElement.props.children).map((l) => {
        if (b.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = L(l.props.el);
          return b.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...b.Children.toArray(l.props.children), ...t]
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
      type: i,
      useCapture: c
    }) => {
      o.addEventListener(i, s, c);
    });
  });
  const r = Array.from(n.childNodes);
  for (let l = 0; l < r.length; l++) {
    const t = r[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = L(t);
      e.push(...i), o.appendChild(s);
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
const T = $(({
  slot: n,
  clone: e,
  className: o,
  style: r
}, l) => {
  const t = O(), [s, i] = G([]);
  return P(() => {
    var f;
    if (!t.current || !n)
      return;
    let c = n;
    function h() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Fe(l, u), o && u.classList.add(...o.split(" ")), r) {
        const _ = je(r);
        Object.keys(_).forEach((p) => {
          u.style[p] = _[p];
        });
      }
    }
    let a = null;
    if (e && window.MutationObserver) {
      let u = function() {
        var g, E, v;
        (g = t.current) != null && g.contains(c) && ((E = t.current) == null || E.removeChild(c));
        const {
          portals: p,
          clonedElement: m
        } = L(n);
        return c = m, i(p), c.style.display = "contents", h(), (v = t.current) == null || v.appendChild(c), p.length > 0;
      };
      u() || (a = new window.MutationObserver(() => {
        u() && (a == null || a.disconnect());
      }), a.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", h(), (f = t.current) == null || f.appendChild(c);
    return () => {
      var u, _;
      c.style.display = "", (u = t.current) != null && u.contains(c) && ((_ = t.current) == null || _.removeChild(c)), a == null || a.disconnect();
    };
  }, [n, e, o, r, l]), b.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(n) {
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
function I(n) {
  return U(() => Le(n), [n]);
}
function Te({
  value: n,
  onValueChange: e
}) {
  const [o, r] = G(n), l = O(e);
  l.current = e;
  const t = O(o);
  return t.current = o, P(() => {
    l.current(o);
  }, [o]), P(() => {
    re(n, t.current) || r(n);
  }, [n]), [o, r];
}
function X(n, e, o) {
  return n.filter(Boolean).map((r, l) => {
    var c;
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const t = {
      ...r.props,
      key: ((c = r.props) == null ? void 0 : c.key) ?? (o ? `${o}-${l}` : `${l}`)
    };
    let s = t;
    Object.keys(r.slots).forEach((h) => {
      if (!r.slots[h] || !(r.slots[h] instanceof Element) && !r.slots[h].el)
        return;
      const a = h.split(".");
      a.forEach((m, g) => {
        s[m] || (s[m] = {}), g !== a.length - 1 && (s = t[m]);
      });
      const f = r.slots[h];
      let u, _, p = (e == null ? void 0 : e.clone) ?? !1;
      f instanceof Element ? u = f : (u = f.el, _ = f.callback, p = f.clone ?? !1), s[a[a.length - 1]] = u ? _ ? (...m) => (_(a[a.length - 1], m), /* @__PURE__ */ w.jsx(T, {
        slot: u,
        clone: p
      })) : /* @__PURE__ */ w.jsx(T, {
        slot: u,
        clone: p
      }) : s[a[a.length - 1]], s = t;
    });
    const i = (e == null ? void 0 : e.children) || "children";
    return r[i] && (t[i] = X(r[i], e, `${l}`)), t;
  });
}
const Ae = Oe(({
  slots: n,
  children: e,
  onValueChange: o,
  filterOption: r,
  onChange: l,
  options: t,
  validateSearch: s,
  optionItems: i,
  getPopupContainer: c,
  elRef: h,
  ...a
}) => {
  const f = I(c), u = I(r), _ = I(s), [p, m] = Te({
    onValueChange: o,
    value: a.value
  });
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ w.jsx(ne, {
      ...a,
      ref: h,
      value: p,
      options: U(() => t || X(i, {
        clone: !0
      }), [i, t]),
      onChange: (g, ...E) => {
        l == null || l(g, ...E), m(g);
      },
      validateSearch: _,
      notFoundContent: n.notFoundContent ? /* @__PURE__ */ w.jsx(T, {
        slot: n.notFoundContent
      }) : a.notFoundContent,
      filterOption: u || r,
      getPopupContainer: f
    })]
  });
});
export {
  Ae as Mentions,
  Ae as default
};
