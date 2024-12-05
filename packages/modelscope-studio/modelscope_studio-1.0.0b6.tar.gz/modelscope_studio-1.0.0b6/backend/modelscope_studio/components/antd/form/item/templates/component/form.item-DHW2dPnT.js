import { g as oe, w as O } from "./Index-B0EXaYU3.js";
const x = window.ms_globals.React, $ = window.ms_globals.React.forwardRef, ee = window.ms_globals.React.useRef, te = window.ms_globals.React.useState, ne = window.ms_globals.React.useEffect, T = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, re = window.ms_globals.internalContext.FormItemContext, le = window.ms_globals.antd.Form;
var q = {
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
var se = x, ie = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ae = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, fe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function B(t, n, s) {
  var r, o = {}, e = null, l = null;
  s !== void 0 && (e = "" + s), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (r in n) ae.call(n, r) && !fe.hasOwnProperty(r) && (o[r] = n[r]);
  if (t && t.defaultProps) for (r in n = t.defaultProps, n) o[r] === void 0 && (o[r] = n[r]);
  return {
    $$typeof: ie,
    type: t,
    key: e,
    ref: l,
    props: o,
    _owner: ue.current
  };
}
P.Fragment = ce;
P.jsx = B;
P.jsxs = B;
q.exports = P;
var h = q.exports;
const {
  SvelteComponent: de,
  assign: A,
  binding_callbacks: N,
  check_outros: pe,
  children: J,
  claim_element: Y,
  claim_space: _e,
  component_subscribe: W,
  compute_slots: me,
  create_slot: he,
  detach: I,
  element: K,
  empty: z,
  exclude_internal_props: D,
  get_all_dirty_from_scope: ge,
  get_slot_changes: be,
  group_outros: we,
  init: Ee,
  insert_hydration: R,
  safe_not_equal: ye,
  set_custom_element_data: Q,
  space: Ce,
  transition_in: j,
  transition_out: F,
  update_slot_base: xe
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: Ie,
  onDestroy: Oe,
  setContext: Re
} = window.__gradio__svelte__internal;
function V(t) {
  let n, s;
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
      n = K("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      n = Y(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = J(n);
      o && o.l(l), l.forEach(I), this.h();
    },
    h() {
      Q(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      R(e, n, l), o && o.m(n, null), t[9](n), s = !0;
    },
    p(e, l) {
      o && o.p && (!s || l & /*$$scope*/
      64) && xe(
        o,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? be(
          r,
          /*$$scope*/
          e[6],
          l,
          null
        ) : ge(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (j(o, e), s = !0);
    },
    o(e) {
      F(o, e), s = !1;
    },
    d(e) {
      e && I(n), o && o.d(e), t[9](null);
    }
  };
}
function je(t) {
  let n, s, r, o, e = (
    /*$$slots*/
    t[4].default && V(t)
  );
  return {
    c() {
      n = K("react-portal-target"), s = Ce(), e && e.c(), r = z(), this.h();
    },
    l(l) {
      n = Y(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(n).forEach(I), s = _e(l), e && e.l(l), r = z(), this.h();
    },
    h() {
      Q(n, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      R(l, n, c), t[8](n), R(l, s, c), e && e.m(l, c), R(l, r, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && j(e, 1)) : (e = V(l), e.c(), j(e, 1), e.m(r.parentNode, r)) : e && (we(), F(e, 1, 1, () => {
        e = null;
      }), pe());
    },
    i(l) {
      o || (j(e), o = !0);
    },
    o(l) {
      F(e), o = !1;
    },
    d(l) {
      l && (I(n), I(s), I(r)), t[8](null), e && e.d(l);
    }
  };
}
function G(t) {
  const {
    svelteInit: n,
    ...s
  } = t;
  return s;
}
function Pe(t, n, s) {
  let r, o, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const c = me(e);
  let {
    svelteInit: i
  } = n;
  const p = O(G(n)), a = O();
  W(t, a, (f) => s(0, r = f));
  const _ = O();
  W(t, _, (f) => s(1, o = f));
  const u = [], d = Ie("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: g,
    subSlotIndex: b
  } = oe() || {}, v = i({
    parent: d,
    props: p,
    target: a,
    slot: _,
    slotKey: m,
    slotIndex: g,
    subSlotIndex: b,
    onDestroy(f) {
      u.push(f);
    }
  });
  Re("$$ms-gr-react-wrapper", v), ve(() => {
    p.set(G(n));
  }), Oe(() => {
    u.forEach((f) => f());
  });
  function E(f) {
    N[f ? "unshift" : "push"](() => {
      r = f, a.set(r);
    });
  }
  function y(f) {
    N[f ? "unshift" : "push"](() => {
      o = f, _.set(o);
    });
  }
  return t.$$set = (f) => {
    s(17, n = A(A({}, n), D(f))), "svelteInit" in f && s(5, i = f.svelteInit), "$$scope" in f && s(6, l = f.$$scope);
  }, n = D(n), [r, o, a, _, c, i, l, e, E, y];
}
class Se extends de {
  constructor(n) {
    super(), Ee(this, n, Pe, je, ye, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, S = window.ms_globals.tree;
function ke(t) {
  function n(s) {
    const r = O(), o = new Se({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? S;
          return c.nodes = [...c.nodes, l], M({
            createPortal: k,
            node: S
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== r), M({
              createPortal: k,
              node: S
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
      s(n);
    });
  });
}
const Fe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Le(t) {
  return t ? Object.keys(t).reduce((n, s) => {
    const r = t[s];
    return typeof r == "number" && !Fe.includes(s) ? n[s] = r + "px" : n[s] = r, n;
  }, {}) : {};
}
function L(t) {
  const n = [], s = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(k(x.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: x.Children.toArray(t._reactElement.props.children).map((o) => {
        if (x.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = L(o.props.el);
          return x.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...x.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, l, i);
    });
  });
  const r = Array.from(t.childNodes);
  for (let o = 0; o < r.length; o++) {
    const e = r[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = L(e);
      n.push(...c), s.appendChild(l);
    } else e.nodeType === 3 && s.appendChild(e.cloneNode());
  }
  return {
    clonedElement: s,
    portals: n
  };
}
function Te(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const w = $(({
  slot: t,
  clone: n,
  className: s,
  style: r
}, o) => {
  const e = ee(), [l, c] = te([]);
  return ne(() => {
    var _;
    if (!e.current || !t)
      return;
    let i = t;
    function p() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Te(o, u), s && u.classList.add(...s.split(" ")), r) {
        const d = Le(r);
        Object.keys(d).forEach((m) => {
          u.style[m] = d[m];
        });
      }
    }
    let a = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var b, v, E;
        (b = e.current) != null && b.contains(i) && ((v = e.current) == null || v.removeChild(i));
        const {
          portals: m,
          clonedElement: g
        } = L(t);
        return i = g, c(m), i.style.display = "contents", p(), (E = e.current) == null || E.appendChild(i), m.length > 0;
      };
      u() || (a = new window.MutationObserver(() => {
        u() && (a == null || a.disconnect());
      }), a.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", p(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var u, d;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((d = e.current) == null || d.removeChild(i)), a == null || a.disconnect();
    };
  }, [t, n, s, r, o]), x.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ae(t) {
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
function C(t) {
  return T(() => Ae(t), [t]);
}
function X(t, n, s) {
  return t.filter(Boolean).map((r, o) => {
    var i;
    if (typeof r != "object")
      return r;
    const e = {
      ...r.props,
      key: ((i = r.props) == null ? void 0 : i.key) ?? (s ? `${s}-${o}` : `${o}`)
    };
    let l = e;
    Object.keys(r.slots).forEach((p) => {
      if (!r.slots[p] || !(r.slots[p] instanceof Element) && !r.slots[p].el)
        return;
      const a = p.split(".");
      a.forEach((g, b) => {
        l[g] || (l[g] = {}), b !== a.length - 1 && (l = e[g]);
      });
      const _ = r.slots[p];
      let u, d, m = !1;
      _ instanceof Element ? u = _ : (u = _.el, d = _.callback, m = _.clone ?? !1), l[a[a.length - 1]] = u ? d ? (...g) => (d(a[a.length - 1], g), /* @__PURE__ */ h.jsx(w, {
        slot: u,
        clone: m
      })) : /* @__PURE__ */ h.jsx(w, {
        slot: u,
        clone: m
      }) : l[a[a.length - 1]], l = e;
    });
    const c = "children";
    return r[c] && (e[c] = X(r[c], n, `${o}`)), e;
  });
}
function H(t) {
  return typeof t == "object" && t !== null ? t : {};
}
const U = ({
  children: t,
  ...n
}) => /* @__PURE__ */ h.jsx(re.Provider, {
  value: T(() => n, [n]),
  children: t
}), We = ke(({
  slots: t,
  getValueFromEvent: n,
  getValueProps: s,
  normalize: r,
  shouldUpdate: o,
  tooltip: e,
  ruleItems: l,
  rules: c,
  children: i,
  hasFeedback: p,
  ...a
}) => {
  const _ = t["tooltip.icon"] || t["tooltip.title"] || typeof e == "object", u = typeof p == "object", d = H(p), m = C(d.icons), g = C(n), b = C(s), v = C(r), E = C(o), y = H(e), f = C(y.afterOpenChange), Z = C(y.getPopupContainer);
  return /* @__PURE__ */ h.jsx(le.Item, {
    ...a,
    hasFeedback: u ? {
      ...d,
      icons: m || d.icons
    } : p,
    getValueFromEvent: g,
    getValueProps: b,
    normalize: v,
    shouldUpdate: E || o,
    rules: T(() => c || X(l), [l, c]),
    tooltip: t.tooltip ? /* @__PURE__ */ h.jsx(w, {
      slot: t.tooltip
    }) : _ ? {
      ...y,
      afterOpenChange: f,
      getPopupContainer: Z,
      icon: t["tooltip.icon"] ? /* @__PURE__ */ h.jsx(w, {
        slot: t["tooltip.icon"]
      }) : y.icon,
      title: t["tooltip.title"] ? /* @__PURE__ */ h.jsx(w, {
        slot: t["tooltip.title"]
      }) : y.title
    } : e,
    extra: t.extra ? /* @__PURE__ */ h.jsx(w, {
      slot: t.extra
    }) : a.extra,
    help: t.help ? /* @__PURE__ */ h.jsx(w, {
      slot: t.help
    }) : a.help,
    label: t.label ? /* @__PURE__ */ h.jsx(w, {
      slot: t.label
    }) : a.label,
    children: E || o ? () => /* @__PURE__ */ h.jsx(U, {
      children: i
    }) : /* @__PURE__ */ h.jsx(U, {
      children: i
    })
  });
});
export {
  We as FormItem,
  We as default
};
