import { g as he, w as k } from "./Index-CEFFmGJj.js";
const E = window.ms_globals.React, fe = window.ms_globals.React.forwardRef, pe = window.ms_globals.React.useRef, _e = window.ms_globals.React.useState, me = window.ms_globals.React.useEffect, g = window.ms_globals.React.useMemo, L = window.ms_globals.ReactDOM.createPortal, ve = window.ms_globals.antd.TimePicker, z = window.ms_globals.dayjs;
var Q = {
  exports: {}
}, D = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var we = E, ye = Symbol.for("react.element"), be = Symbol.for("react.fragment"), ge = Object.prototype.hasOwnProperty, xe = we.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function X(e, t, o) {
  var l, r = {}, n = null, s = null;
  o !== void 0 && (n = "" + o), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ge.call(t, l) && !Ee.hasOwnProperty(l) && (r[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: ye,
    type: e,
    key: n,
    ref: s,
    props: r,
    _owner: xe.current
  };
}
D.Fragment = be;
D.jsx = X;
D.jsxs = X;
Q.exports = D;
var p = Q.exports;
const {
  SvelteComponent: Ie,
  assign: G,
  binding_callbacks: U,
  check_outros: Re,
  children: Z,
  claim_element: $,
  claim_space: Pe,
  component_subscribe: H,
  compute_slots: Se,
  create_slot: Ce,
  detach: S,
  element: ee,
  empty: K,
  exclude_internal_props: V,
  get_all_dirty_from_scope: je,
  get_slot_changes: Oe,
  group_outros: ke,
  init: Fe,
  insert_hydration: F,
  safe_not_equal: Te,
  set_custom_element_data: te,
  space: De,
  transition_in: T,
  transition_out: M,
  update_slot_base: Ne
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ae,
  getContext: Le,
  onDestroy: Me,
  setContext: We
} = window.__gradio__svelte__internal;
function q(e) {
  let t, o;
  const l = (
    /*#slots*/
    e[7].default
  ), r = Ce(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = ee("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      t = $(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = Z(t);
      r && r.l(s), s.forEach(S), this.h();
    },
    h() {
      te(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      F(n, t, s), r && r.m(t, null), e[9](t), o = !0;
    },
    p(n, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && Ne(
        r,
        l,
        n,
        /*$$scope*/
        n[6],
        o ? Oe(
          l,
          /*$$scope*/
          n[6],
          s,
          null
        ) : je(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (T(r, n), o = !0);
    },
    o(n) {
      M(r, n), o = !1;
    },
    d(n) {
      n && S(t), r && r.d(n), e[9](null);
    }
  };
}
function ze(e) {
  let t, o, l, r, n = (
    /*$$slots*/
    e[4].default && q(e)
  );
  return {
    c() {
      t = ee("react-portal-target"), o = De(), n && n.c(), l = K(), this.h();
    },
    l(s) {
      t = $(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Z(t).forEach(S), o = Pe(s), n && n.l(s), l = K(), this.h();
    },
    h() {
      te(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      F(s, t, c), e[8](t), F(s, o, c), n && n.m(s, c), F(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, c), c & /*$$slots*/
      16 && T(n, 1)) : (n = q(s), n.c(), T(n, 1), n.m(l.parentNode, l)) : n && (ke(), M(n, 1, 1, () => {
        n = null;
      }), Re());
    },
    i(s) {
      r || (T(n), r = !0);
    },
    o(s) {
      M(n), r = !1;
    },
    d(s) {
      s && (S(t), S(o), S(l)), e[8](null), n && n.d(s);
    }
  };
}
function B(e) {
  const {
    svelteInit: t,
    ...o
  } = e;
  return o;
}
function Ge(e, t, o) {
  let l, r, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const c = Se(n);
  let {
    svelteInit: i
  } = t;
  const h = k(B(t)), d = k();
  H(e, d, (a) => o(0, l = a));
  const v = k();
  H(e, v, (a) => o(1, r = a));
  const u = [], _ = Le("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: y,
    subSlotIndex: I
  } = he() || {}, b = i({
    parent: _,
    props: h,
    target: d,
    slot: v,
    slotKey: f,
    slotIndex: y,
    subSlotIndex: I,
    onDestroy(a) {
      u.push(a);
    }
  });
  We("$$ms-gr-react-wrapper", b), Ae(() => {
    h.set(B(t));
  }), Me(() => {
    u.forEach((a) => a());
  });
  function R(a) {
    U[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function m(a) {
    U[a ? "unshift" : "push"](() => {
      r = a, v.set(r);
    });
  }
  return e.$$set = (a) => {
    o(17, t = G(G({}, t), V(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, t = V(t), [l, r, d, v, c, i, s, n, R, m];
}
class Ue extends Ie {
  constructor(t) {
    super(), Fe(this, t, Ge, ze, Te, {
      svelteInit: 5
    });
  }
}
const J = window.ms_globals.rerender, N = window.ms_globals.tree;
function He(e) {
  function t(o) {
    const l = k(), r = new Ue({
      ...o,
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
          }, c = n.parent ?? N;
          return c.nodes = [...c.nodes, s], J({
            createPortal: L,
            node: N
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), J({
              createPortal: L,
              node: N
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
      o(t);
    });
  });
}
const Ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ve(e) {
  return e ? Object.keys(e).reduce((t, o) => {
    const l = e[o];
    return typeof l == "number" && !Ke.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function W(e) {
  const t = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(L(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((r) => {
        if (E.isValidElement(r) && r.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = W(r.props.el);
          return E.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...E.Children.toArray(r.props.children), ...n]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let r = 0; r < l.length; r++) {
    const n = l[r];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = W(n);
      t.push(...c), o.appendChild(s);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function qe(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const w = fe(({
  slot: e,
  clone: t,
  className: o,
  style: l
}, r) => {
  const n = pe(), [s, c] = _e([]);
  return me(() => {
    var v;
    if (!n.current || !e)
      return;
    let i = e;
    function h() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), qe(r, u), o && u.classList.add(...o.split(" ")), l) {
        const _ = Ve(l);
        Object.keys(_).forEach((f) => {
          u.style[f] = _[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var I, b, R;
        (I = n.current) != null && I.contains(i) && ((b = n.current) == null || b.removeChild(i));
        const {
          portals: f,
          clonedElement: y
        } = W(e);
        return i = y, c(f), i.style.display = "contents", h(), (R = n.current) == null || R.appendChild(i), f.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", h(), (v = n.current) == null || v.appendChild(i);
    return () => {
      var u, _;
      i.style.display = "", (u = n.current) != null && u.contains(i) && ((_ = n.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, t, o, l, r]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Be(e) {
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
function O(e) {
  return g(() => Be(e), [e]);
}
function Je(e, t) {
  return e ? /* @__PURE__ */ p.jsx(w, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Y({
  key: e,
  setSlotParams: t,
  slots: o
}, l) {
  return o[e] ? (...r) => (t(e, r), Je(o[e], {
    clone: !0,
    ...l
  })) : void 0;
}
function x(e) {
  return Array.isArray(e) ? e.map((t) => x(t)) : z(typeof e == "number" ? e * 1e3 : e);
}
function A(e) {
  return Array.isArray(e) ? e.map((t) => t ? t.valueOf() / 1e3 : null) : typeof e == "object" && e !== null ? e.valueOf() / 1e3 : e;
}
const Qe = He(({
  slots: e,
  disabledDate: t,
  disabledTime: o,
  value: l,
  defaultValue: r,
  defaultPickerValue: n,
  pickerValue: s,
  onChange: c,
  minDate: i,
  maxDate: h,
  cellRender: d,
  panelRender: v,
  getPopupContainer: u,
  onValueChange: _,
  onPanelChange: f,
  onCalendarChange: y,
  children: I,
  setSlotParams: b,
  elRef: R,
  ...m
}) => {
  const a = O(t), ne = O(o), re = O(u), oe = O(d), le = O(v), se = g(() => l ? x(l) : void 0, [l]), ie = g(() => r ? x(r) : void 0, [r]), ce = g(() => n ? x(n) : void 0, [n]), ae = g(() => s ? x(s) : void 0, [s]), ue = g(() => i ? x(i) : void 0, [i]), de = g(() => h ? x(h) : void 0, [h]);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: I
    }), /* @__PURE__ */ p.jsx(ve, {
      ...m,
      ref: R,
      value: se,
      defaultValue: ie,
      defaultPickerValue: ce,
      pickerValue: ae,
      minDate: ue,
      maxDate: de,
      disabledTime: ne,
      disabledDate: a,
      getPopupContainer: re,
      cellRender: e.cellRender ? Y({
        slots: e,
        setSlotParams: b,
        key: "cellRender"
      }) : oe,
      panelRender: e.panelRender ? Y({
        slots: e,
        setSlotParams: b,
        key: "panelRender"
      }) : le,
      onPanelChange: (C, ...j) => {
        const P = A(C);
        f == null || f(P, ...j);
      },
      onChange: (C, ...j) => {
        const P = A(C);
        c == null || c(P, ...j), _(P);
      },
      onCalendarChange: (C, ...j) => {
        const P = A(C);
        y == null || y(P, ...j);
      },
      renderExtraFooter: e.renderExtraFooter ? () => e.renderExtraFooter ? /* @__PURE__ */ p.jsx(w, {
        slot: e.renderExtraFooter
      }) : null : m.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ p.jsx(w, {
        slot: e.prevIcon
      }) : m.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ p.jsx(w, {
        slot: e.nextIcon
      }) : m.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ p.jsx(w, {
        slot: e.suffixIcon
      }) : m.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ p.jsx(w, {
        slot: e.superNextIcon
      }) : m.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ p.jsx(w, {
        slot: e.superPrevIcon
      }) : m.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ p.jsx(w, {
          slot: e["allowClear.clearIcon"]
        })
      } : m.allowClear
    })]
  });
});
export {
  Qe as TimePicker,
  Qe as default
};
