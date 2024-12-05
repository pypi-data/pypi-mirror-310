import { g as ye, w as P } from "./Index-DWQ5yMxy.js";
const I = window.ms_globals.React, he = window.ms_globals.React.forwardRef, ve = window.ms_globals.React.useRef, ge = window.ms_globals.React.useState, be = window.ms_globals.React.useEffect, g = window.ms_globals.React.useMemo, M = window.ms_globals.ReactDOM.createPortal, we = window.ms_globals.antd.DatePicker, z = window.ms_globals.dayjs;
var X = {
  exports: {}
}, N = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var xe = I, Ee = Symbol.for("react.element"), Ie = Symbol.for("react.fragment"), Re = Object.prototype.hasOwnProperty, Ce = xe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, je = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Z(e, t, s) {
  var r, o = {}, n = null, l = null;
  s !== void 0 && (n = "" + s), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t) Re.call(t, r) && !je.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: Ee,
    type: e,
    key: n,
    ref: l,
    props: o,
    _owner: Ce.current
  };
}
N.Fragment = Ie;
N.jsx = Z;
N.jsxs = Z;
X.exports = N;
var h = X.exports;
const {
  SvelteComponent: ke,
  assign: G,
  binding_callbacks: U,
  check_outros: Se,
  children: $,
  claim_element: ee,
  claim_space: Oe,
  component_subscribe: H,
  compute_slots: Pe,
  create_slot: De,
  detach: j,
  element: te,
  empty: q,
  exclude_internal_props: B,
  get_all_dirty_from_scope: Fe,
  get_slot_changes: Ne,
  group_outros: Ae,
  init: Le,
  insert_hydration: D,
  safe_not_equal: Te,
  set_custom_element_data: ne,
  space: Me,
  transition_in: F,
  transition_out: W,
  update_slot_base: We
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ve,
  getContext: ze,
  onDestroy: Ge,
  setContext: Ue
} = window.__gradio__svelte__internal;
function J(e) {
  let t, s;
  const r = (
    /*#slots*/
    e[7].default
  ), o = De(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = te("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = ee(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = $(t);
      o && o.l(l), l.forEach(j), this.h();
    },
    h() {
      ne(t, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      D(n, t, l), o && o.m(t, null), e[9](t), s = !0;
    },
    p(n, l) {
      o && o.p && (!s || l & /*$$scope*/
      64) && We(
        o,
        r,
        n,
        /*$$scope*/
        n[6],
        s ? Ne(
          r,
          /*$$scope*/
          n[6],
          l,
          null
        ) : Fe(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      s || (F(o, n), s = !0);
    },
    o(n) {
      W(o, n), s = !1;
    },
    d(n) {
      n && j(t), o && o.d(n), e[9](null);
    }
  };
}
function He(e) {
  let t, s, r, o, n = (
    /*$$slots*/
    e[4].default && J(e)
  );
  return {
    c() {
      t = te("react-portal-target"), s = Me(), n && n.c(), r = q(), this.h();
    },
    l(l) {
      t = ee(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(t).forEach(j), s = Oe(l), n && n.l(l), r = q(), this.h();
    },
    h() {
      ne(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      D(l, t, c), e[8](t), D(l, s, c), n && n.m(l, c), D(l, r, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, c), c & /*$$slots*/
      16 && F(n, 1)) : (n = J(l), n.c(), F(n, 1), n.m(r.parentNode, r)) : n && (Ae(), W(n, 1, 1, () => {
        n = null;
      }), Se());
    },
    i(l) {
      o || (F(n), o = !0);
    },
    o(l) {
      W(n), o = !1;
    },
    d(l) {
      l && (j(t), j(s), j(r)), e[8](null), n && n.d(l);
    }
  };
}
function Y(e) {
  const {
    svelteInit: t,
    ...s
  } = e;
  return s;
}
function qe(e, t, s) {
  let r, o, {
    $$slots: n = {},
    $$scope: l
  } = t;
  const c = Pe(n);
  let {
    svelteInit: i
  } = t;
  const p = P(Y(t)), u = P();
  H(e, u, (d) => s(0, r = d));
  const f = P();
  H(e, f, (d) => s(1, o = d));
  const a = [], _ = ze("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: v,
    subSlotIndex: w
  } = ye() || {}, x = i({
    parent: _,
    props: p,
    target: u,
    slot: f,
    slotKey: m,
    slotIndex: v,
    subSlotIndex: w,
    onDestroy(d) {
      a.push(d);
    }
  });
  Ue("$$ms-gr-react-wrapper", x), Ve(() => {
    p.set(Y(t));
  }), Ge(() => {
    a.forEach((d) => d());
  });
  function R(d) {
    U[d ? "unshift" : "push"](() => {
      r = d, u.set(r);
    });
  }
  function k(d) {
    U[d ? "unshift" : "push"](() => {
      o = d, f.set(o);
    });
  }
  return e.$$set = (d) => {
    s(17, t = G(G({}, t), B(d))), "svelteInit" in d && s(5, i = d.svelteInit), "$$scope" in d && s(6, l = d.$$scope);
  }, t = B(t), [r, o, u, f, c, i, l, n, R, k];
}
class Be extends ke {
  constructor(t) {
    super(), Le(this, t, qe, He, Te, {
      svelteInit: 5
    });
  }
}
const K = window.ms_globals.rerender, L = window.ms_globals.tree;
function Je(e) {
  function t(s) {
    const r = P(), o = new Be({
      ...s,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? L;
          return c.nodes = [...c.nodes, l], K({
            createPortal: M,
            node: L
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== r), K({
              createPortal: M,
              node: L
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
      s(t);
    });
  });
}
const Ye = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ke(e) {
  return e ? Object.keys(e).reduce((t, s) => {
    const r = e[s];
    return typeof r == "number" && !Ye.includes(s) ? t[s] = r + "px" : t[s] = r, t;
  }, {}) : {};
}
function V(e) {
  const t = [], s = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(M(I.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: I.Children.toArray(e._reactElement.props.children).map((o) => {
        if (I.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: l
          } = V(o.props.el);
          return I.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...I.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, l, i);
    });
  });
  const r = Array.from(e.childNodes);
  for (let o = 0; o < r.length; o++) {
    const n = r[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = V(n);
      t.push(...c), s.appendChild(l);
    } else n.nodeType === 3 && s.appendChild(n.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function Qe(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const y = he(({
  slot: e,
  clone: t,
  className: s,
  style: r
}, o) => {
  const n = ve(), [l, c] = ge([]);
  return be(() => {
    var f;
    if (!n.current || !e)
      return;
    let i = e;
    function p() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Qe(o, a), s && a.classList.add(...s.split(" ")), r) {
        const _ = Ke(r);
        Object.keys(_).forEach((m) => {
          a.style[m] = _[m];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var w, x, R;
        (w = n.current) != null && w.contains(i) && ((x = n.current) == null || x.removeChild(i));
        const {
          portals: m,
          clonedElement: v
        } = V(e);
        return i = v, c(m), i.style.display = "contents", p(), (R = n.current) == null || R.appendChild(i), m.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", p(), (f = n.current) == null || f.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = n.current) != null && a.contains(i) && ((_ = n.current) == null || _.removeChild(i)), u == null || u.disconnect();
    };
  }, [e, t, s, r, o]), I.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Xe(e) {
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
function S(e) {
  return g(() => Xe(e), [e]);
}
function re(e, t, s) {
  return e.filter(Boolean).map((r, o) => {
    var i;
    if (typeof r != "object")
      return r;
    const n = {
      ...r.props,
      key: ((i = r.props) == null ? void 0 : i.key) ?? (s ? `${s}-${o}` : `${o}`)
    };
    let l = n;
    Object.keys(r.slots).forEach((p) => {
      if (!r.slots[p] || !(r.slots[p] instanceof Element) && !r.slots[p].el)
        return;
      const u = p.split(".");
      u.forEach((v, w) => {
        l[v] || (l[v] = {}), w !== u.length - 1 && (l = n[v]);
      });
      const f = r.slots[p];
      let a, _, m = !1;
      f instanceof Element ? a = f : (a = f.el, _ = f.callback, m = f.clone ?? !1), l[u[u.length - 1]] = a ? _ ? (...v) => (_(u[u.length - 1], v), /* @__PURE__ */ h.jsx(y, {
        slot: a,
        clone: m
      })) : /* @__PURE__ */ h.jsx(y, {
        slot: a,
        clone: m
      }) : l[u[u.length - 1]], l = n;
    });
    const c = "children";
    return r[c] && (n[c] = re(r[c], t, `${o}`)), n;
  });
}
function Ze(e, t) {
  return e ? /* @__PURE__ */ h.jsx(y, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function T({
  key: e,
  setSlotParams: t,
  slots: s
}, r) {
  return s[e] ? (...o) => (t(e, o), Ze(s[e], {
    clone: !0,
    ...r
  })) : void 0;
}
function b(e) {
  return Array.isArray(e) ? e.map((t) => b(t)) : z(typeof e == "number" ? e * 1e3 : e);
}
function Q(e) {
  return Array.isArray(e) ? e.map((t) => t ? t.valueOf() / 1e3 : null) : typeof e == "object" && e !== null ? e.valueOf() / 1e3 : e;
}
const et = Je(({
  slots: e,
  disabledDate: t,
  disabledTime: s,
  value: r,
  defaultValue: o,
  defaultPickerValue: n,
  pickerValue: l,
  showTime: c,
  presets: i,
  presetItems: p,
  onChange: u,
  minDate: f,
  maxDate: a,
  cellRender: _,
  panelRender: m,
  getPopupContainer: v,
  onValueChange: w,
  onPanelChange: x,
  children: R,
  setSlotParams: k,
  elRef: d,
  ...E
}) => {
  const oe = S(t), le = S(s), se = S(v), ce = S(_), ie = S(m), ae = g(() => typeof c == "object" ? {
    ...c,
    defaultValue: c.defaultValue ? b(c.defaultValue) : void 0
  } : c, [c]), ue = g(() => r ? b(r) : void 0, [r]), de = g(() => o ? b(o) : void 0, [o]), fe = g(() => n ? b(n) : void 0, [n]), pe = g(() => l ? b(l) : void 0, [l]), _e = g(() => f ? b(f) : void 0, [f]), me = g(() => a ? b(a) : void 0, [a]);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: R
    }), /* @__PURE__ */ h.jsx(we, {
      ...E,
      ref: d,
      value: ue,
      defaultValue: de,
      defaultPickerValue: fe,
      pickerValue: pe,
      minDate: _e,
      maxDate: me,
      showTime: ae,
      disabledDate: oe,
      disabledTime: le,
      getPopupContainer: se,
      cellRender: e.cellRender ? T({
        slots: e,
        setSlotParams: k,
        key: "cellRender"
      }) : ce,
      panelRender: e.panelRender ? T({
        slots: e,
        setSlotParams: k,
        key: "panelRender"
      }) : ie,
      presets: g(() => (i || re(p)).map((C) => ({
        ...C,
        value: b(C.value)
      })), [i, p]),
      onPanelChange: (C, ...A) => {
        const O = Q(C);
        x == null || x(O, ...A);
      },
      onChange: (C, ...A) => {
        const O = Q(C);
        u == null || u(O, ...A), w(O);
      },
      renderExtraFooter: e.renderExtraFooter ? T({
        slots: e,
        setSlotParams: k,
        key: "renderExtraFooter"
      }) : E.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ h.jsx(y, {
        slot: e.prevIcon
      }) : E.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ h.jsx(y, {
        slot: e.nextIcon
      }) : E.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ h.jsx(y, {
        slot: e.suffixIcon
      }) : E.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ h.jsx(y, {
        slot: e.superNextIcon
      }) : E.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ h.jsx(y, {
        slot: e.superPrevIcon
      }) : E.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ h.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : E.allowClear
    })]
  });
});
export {
  et as DatePicker,
  et as default
};
