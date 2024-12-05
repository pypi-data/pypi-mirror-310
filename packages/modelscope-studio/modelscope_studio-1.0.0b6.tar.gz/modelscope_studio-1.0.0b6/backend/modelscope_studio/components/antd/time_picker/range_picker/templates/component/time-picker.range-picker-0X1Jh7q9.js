import { g as he, w as k } from "./Index-DQsaYRAk.js";
const I = window.ms_globals.React, fe = window.ms_globals.React.forwardRef, pe = window.ms_globals.React.useRef, _e = window.ms_globals.React.useState, me = window.ms_globals.React.useEffect, E = window.ms_globals.React.useMemo, L = window.ms_globals.ReactDOM.createPortal, we = window.ms_globals.antd.TimePicker, z = window.ms_globals.dayjs;
var X = {
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
var ge = I, ye = Symbol.for("react.element"), ve = Symbol.for("react.fragment"), be = Object.prototype.hasOwnProperty, xe = ge.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Z(e, t, o) {
  var l, r = {}, n = null, s = null;
  o !== void 0 && (n = "" + o), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) be.call(t, l) && !Ee.hasOwnProperty(l) && (r[l] = t[l]);
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
D.Fragment = ve;
D.jsx = Z;
D.jsxs = Z;
X.exports = D;
var p = X.exports;
const {
  SvelteComponent: Ie,
  assign: G,
  binding_callbacks: U,
  check_outros: Re,
  children: V,
  claim_element: $,
  claim_space: Se,
  component_subscribe: H,
  compute_slots: Pe,
  create_slot: Ce,
  detach: C,
  element: ee,
  empty: K,
  exclude_internal_props: q,
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
function B(e) {
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
      var s = V(t);
      r && r.l(s), s.forEach(C), this.h();
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
      n && C(t), r && r.d(n), e[9](null);
    }
  };
}
function ze(e) {
  let t, o, l, r, n = (
    /*$$slots*/
    e[4].default && B(e)
  );
  return {
    c() {
      t = ee("react-portal-target"), o = De(), n && n.c(), l = K(), this.h();
    },
    l(s) {
      t = $(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), V(t).forEach(C), o = Se(s), n && n.l(s), l = K(), this.h();
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
      16 && T(n, 1)) : (n = B(s), n.c(), T(n, 1), n.m(l.parentNode, l)) : n && (ke(), M(n, 1, 1, () => {
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
      s && (C(t), C(o), C(l)), e[8](null), n && n.d(s);
    }
  };
}
function J(e) {
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
  const c = Pe(n);
  let {
    svelteInit: i
  } = t;
  const w = k(J(t)), d = k();
  H(e, d, (a) => o(0, l = a));
  const g = k();
  H(e, g, (a) => o(1, r = a));
  const u = [], h = Le("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: R
  } = he() || {}, x = i({
    parent: h,
    props: w,
    target: d,
    slot: g,
    slotKey: _,
    slotIndex: b,
    subSlotIndex: R,
    onDestroy(a) {
      u.push(a);
    }
  });
  We("$$ms-gr-react-wrapper", x), Ae(() => {
    w.set(J(t));
  }), Me(() => {
    u.forEach((a) => a());
  });
  function S(a) {
    U[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function m(a) {
    U[a ? "unshift" : "push"](() => {
      r = a, g.set(r);
    });
  }
  return e.$$set = (a) => {
    o(17, t = G(G({}, t), q(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, t = q(t), [l, r, d, g, c, i, s, n, S, m];
}
class Ue extends Ie {
  constructor(t) {
    super(), Fe(this, t, Ge, ze, Te, {
      svelteInit: 5
    });
  }
}
const Y = window.ms_globals.rerender, N = window.ms_globals.tree;
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
          return c.nodes = [...c.nodes, s], Y({
            createPortal: L,
            node: N
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), Y({
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
function qe(e) {
  return e ? Object.keys(e).reduce((t, o) => {
    const l = e[o];
    return typeof l == "number" && !Ke.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function W(e) {
  const t = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(L(I.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: I.Children.toArray(e._reactElement.props.children).map((r) => {
        if (I.isValidElement(r) && r.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = W(r.props.el);
          return I.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...I.Children.toArray(r.props.children), ...n]
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
function Be(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const y = fe(({
  slot: e,
  clone: t,
  className: o,
  style: l
}, r) => {
  const n = pe(), [s, c] = _e([]);
  return me(() => {
    var g;
    if (!n.current || !e)
      return;
    let i = e;
    function w() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Be(r, u), o && u.classList.add(...o.split(" ")), l) {
        const h = qe(l);
        Object.keys(h).forEach((_) => {
          u.style[_] = h[_];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var R, x, S;
        (R = n.current) != null && R.contains(i) && ((x = n.current) == null || x.removeChild(i));
        const {
          portals: _,
          clonedElement: b
        } = W(e);
        return i = b, c(_), i.style.display = "contents", w(), (S = n.current) == null || S.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (g = n.current) == null || g.appendChild(i);
    return () => {
      var u, h;
      i.style.display = "", (u = n.current) != null && u.contains(i) && ((h = n.current) == null || h.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, t, o, l, r]), I.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Je(e) {
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
  return E(() => Je(e), [e]);
}
function Ye(e, t) {
  return e ? /* @__PURE__ */ p.jsx(y, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Q({
  key: e,
  setSlotParams: t,
  slots: o
}, l) {
  return o[e] ? (...r) => (t(e, r), Ye(o[e], {
    clone: !0,
    ...l
  })) : void 0;
}
function v(e) {
  return z(typeof e == "number" ? e * 1e3 : e);
}
function A(e) {
  return (e == null ? void 0 : e.map((t) => t ? t.valueOf() / 1e3 : null)) || [null, null];
}
const Xe = He(({
  slots: e,
  disabledDate: t,
  disabledTime: o,
  value: l,
  defaultValue: r,
  defaultPickerValue: n,
  pickerValue: s,
  onChange: c,
  minDate: i,
  maxDate: w,
  cellRender: d,
  panelRender: g,
  getPopupContainer: u,
  onValueChange: h,
  onPanelChange: _,
  onCalendarChange: b,
  children: R,
  setSlotParams: x,
  elRef: S,
  ...m
}) => {
  const a = O(t), ne = O(u), re = O(d), oe = O(g), se = O(o), le = E(() => l == null ? void 0 : l.map((f) => v(f)), [l]), ie = E(() => r == null ? void 0 : r.map((f) => v(f)), [r]), ce = E(() => Array.isArray(n) ? n.map((f) => v(f)) : n ? v(n) : void 0, [n]), ae = E(() => Array.isArray(s) ? s.map((f) => v(f)) : s ? v(s) : void 0, [s]), ue = E(() => i ? v(i) : void 0, [i]), de = E(() => w ? v(w) : void 0, [w]);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: R
    }), /* @__PURE__ */ p.jsx(we.RangePicker, {
      ...m,
      ref: S,
      value: le,
      disabledTime: se,
      defaultValue: ie,
      defaultPickerValue: ce,
      pickerValue: ae,
      minDate: ue,
      maxDate: de,
      disabledDate: a,
      getPopupContainer: ne,
      cellRender: e.cellRender ? Q({
        slots: e,
        setSlotParams: x,
        key: "cellRender"
      }) : re,
      panelRender: e.panelRender ? Q({
        slots: e,
        setSlotParams: x,
        key: "panelRender"
      }) : oe,
      onPanelChange: (f, ...j) => {
        const P = A(f);
        _ == null || _(P, ...j);
      },
      onChange: (f, ...j) => {
        const P = A(f);
        c == null || c(P, ...j), h(P);
      },
      onCalendarChange: (f, ...j) => {
        const P = A(f);
        b == null || b(P, ...j);
      },
      renderExtraFooter: e.renderExtraFooter ? () => e.renderExtraFooter ? /* @__PURE__ */ p.jsx(y, {
        slot: e.renderExtraFooter
      }) : null : m.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ p.jsx(y, {
        slot: e.prevIcon
      }) : m.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ p.jsx(y, {
        slot: e.nextIcon
      }) : m.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ p.jsx(y, {
        slot: e.suffixIcon
      }) : m.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ p.jsx(y, {
        slot: e.superNextIcon
      }) : m.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ p.jsx(y, {
        slot: e.superPrevIcon
      }) : m.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ p.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : m.allowClear,
      separator: e.separator ? /* @__PURE__ */ p.jsx(y, {
        slot: e.separator
      }) : m.separator
    })]
  });
});
export {
  Xe as TimeRangePicker,
  Xe as default
};
