import { g as ve, w as F } from "./Index-tR_Cinhr.js";
const j = window.ms_globals.React, me = window.ms_globals.React.forwardRef, he = window.ms_globals.React.useRef, ge = window.ms_globals.React.useState, we = window.ms_globals.React.useEffect, E = window.ms_globals.React.useMemo, W = window.ms_globals.ReactDOM.createPortal, ye = window.ms_globals.antd.DatePicker, U = window.ms_globals.dayjs;
var Z = {
  exports: {}
}, L = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var be = j, xe = Symbol.for("react.element"), Ee = Symbol.for("react.fragment"), Ie = Object.prototype.hasOwnProperty, Re = be.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, je = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, n, l) {
  var r, o = {}, t = null, s = null;
  l !== void 0 && (t = "" + l), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (r in n) Ie.call(n, r) && !je.hasOwnProperty(r) && (o[r] = n[r]);
  if (e && e.defaultProps) for (r in n = e.defaultProps, n) o[r] === void 0 && (o[r] = n[r]);
  return {
    $$typeof: xe,
    type: e,
    key: t,
    ref: s,
    props: o,
    _owner: Re.current
  };
}
L.Fragment = Ee;
L.jsx = V;
L.jsxs = V;
Z.exports = L;
var g = Z.exports;
const {
  SvelteComponent: Se,
  assign: H,
  binding_callbacks: q,
  check_outros: Oe,
  children: $,
  claim_element: ee,
  claim_space: Pe,
  component_subscribe: B,
  compute_slots: ke,
  create_slot: Ce,
  detach: P,
  element: te,
  empty: J,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: De,
  get_slot_changes: Fe,
  group_outros: Ne,
  init: Ae,
  insert_hydration: N,
  safe_not_equal: Le,
  set_custom_element_data: ne,
  space: Te,
  transition_in: A,
  transition_out: z,
  update_slot_base: Me
} = window.__gradio__svelte__internal, {
  beforeUpdate: We,
  getContext: ze,
  onDestroy: Ge,
  setContext: Ue
} = window.__gradio__svelte__internal;
function K(e) {
  let n, l;
  const r = (
    /*#slots*/
    e[7].default
  ), o = Ce(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = te("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      n = ee(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = $(n);
      o && o.l(s), s.forEach(P), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      N(t, n, s), o && o.m(n, null), e[9](n), l = !0;
    },
    p(t, s) {
      o && o.p && (!l || s & /*$$scope*/
      64) && Me(
        o,
        r,
        t,
        /*$$scope*/
        t[6],
        l ? Fe(
          r,
          /*$$scope*/
          t[6],
          s,
          null
        ) : De(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      l || (A(o, t), l = !0);
    },
    o(t) {
      z(o, t), l = !1;
    },
    d(t) {
      t && P(n), o && o.d(t), e[9](null);
    }
  };
}
function He(e) {
  let n, l, r, o, t = (
    /*$$slots*/
    e[4].default && K(e)
  );
  return {
    c() {
      n = te("react-portal-target"), l = Te(), t && t.c(), r = J(), this.h();
    },
    l(s) {
      n = ee(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(n).forEach(P), l = Pe(s), t && t.l(s), r = J(), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      N(s, n, i), e[8](n), N(s, l, i), t && t.m(s, i), N(s, r, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, i), i & /*$$slots*/
      16 && A(t, 1)) : (t = K(s), t.c(), A(t, 1), t.m(r.parentNode, r)) : t && (Ne(), z(t, 1, 1, () => {
        t = null;
      }), Oe());
    },
    i(s) {
      o || (A(t), o = !0);
    },
    o(s) {
      z(t), o = !1;
    },
    d(s) {
      s && (P(n), P(l), P(r)), e[8](null), t && t.d(s);
    }
  };
}
function Q(e) {
  const {
    svelteInit: n,
    ...l
  } = e;
  return l;
}
function qe(e, n, l) {
  let r, o, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const i = ke(t);
  let {
    svelteInit: c
  } = n;
  const _ = F(Q(n)), a = F();
  B(e, a, (d) => l(0, r = d));
  const p = F();
  B(e, p, (d) => l(1, o = d));
  const u = [], m = ze("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: w,
    subSlotIndex: v
  } = ve() || {}, I = c({
    parent: m,
    props: _,
    target: a,
    slot: p,
    slotKey: h,
    slotIndex: w,
    subSlotIndex: v,
    onDestroy(d) {
      u.push(d);
    }
  });
  Ue("$$ms-gr-react-wrapper", I), We(() => {
    _.set(Q(n));
  }), Ge(() => {
    u.forEach((d) => d());
  });
  function S(d) {
    q[d ? "unshift" : "push"](() => {
      r = d, a.set(r);
    });
  }
  function k(d) {
    q[d ? "unshift" : "push"](() => {
      o = d, p.set(o);
    });
  }
  return e.$$set = (d) => {
    l(17, n = H(H({}, n), Y(d))), "svelteInit" in d && l(5, c = d.svelteInit), "$$scope" in d && l(6, s = d.$$scope);
  }, n = Y(n), [r, o, a, p, i, c, s, t, S, k];
}
class Be extends Se {
  constructor(n) {
    super(), Ae(this, n, qe, He, Le, {
      svelteInit: 5
    });
  }
}
const X = window.ms_globals.rerender, T = window.ms_globals.tree;
function Je(e) {
  function n(l) {
    const r = F(), o = new Be({
      ...l,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? T;
          return i.nodes = [...i.nodes, s], X({
            createPortal: W,
            node: T
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== r), X({
              createPortal: W,
              node: T
            });
          }), s;
        },
        ...l.props
      }
    });
    return r.set(o), o;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(n);
    });
  });
}
const Ye = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ke(e) {
  return e ? Object.keys(e).reduce((n, l) => {
    const r = e[l];
    return typeof r == "number" && !Ye.includes(l) ? n[l] = r + "px" : n[l] = r, n;
  }, {}) : {};
}
function G(e) {
  const n = [], l = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(W(j.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: j.Children.toArray(e._reactElement.props.children).map((o) => {
        if (j.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = G(o.props.el);
          return j.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...j.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), l)), {
      clonedElement: l,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: i,
      useCapture: c
    }) => {
      l.addEventListener(i, s, c);
    });
  });
  const r = Array.from(e.childNodes);
  for (let o = 0; o < r.length; o++) {
    const t = r[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = G(t);
      n.push(...i), l.appendChild(s);
    } else t.nodeType === 3 && l.appendChild(t.cloneNode());
  }
  return {
    clonedElement: l,
    portals: n
  };
}
function Qe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const y = me(({
  slot: e,
  clone: n,
  className: l,
  style: r
}, o) => {
  const t = he(), [s, i] = ge([]);
  return we(() => {
    var p;
    if (!t.current || !e)
      return;
    let c = e;
    function _() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Qe(o, u), l && u.classList.add(...l.split(" ")), r) {
        const m = Ke(r);
        Object.keys(m).forEach((h) => {
          u.style[h] = m[h];
        });
      }
    }
    let a = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var v, I, S;
        (v = t.current) != null && v.contains(c) && ((I = t.current) == null || I.removeChild(c));
        const {
          portals: h,
          clonedElement: w
        } = G(e);
        return c = w, i(h), c.style.display = "contents", _(), (S = t.current) == null || S.appendChild(c), h.length > 0;
      };
      u() || (a = new window.MutationObserver(() => {
        u() && (a == null || a.disconnect());
      }), a.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", _(), (p = t.current) == null || p.appendChild(c);
    return () => {
      var u, m;
      c.style.display = "", (u = t.current) != null && u.contains(c) && ((m = t.current) == null || m.removeChild(c)), a == null || a.disconnect();
    };
  }, [e, n, l, r, o]), j.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Xe(e) {
  try {
    if (typeof e == "string") {
      let n = e.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function C(e) {
  return E(() => Xe(e), [e]);
}
function re(e, n, l) {
  return e.filter(Boolean).map((r, o) => {
    var c;
    if (typeof r != "object")
      return r;
    const t = {
      ...r.props,
      key: ((c = r.props) == null ? void 0 : c.key) ?? (l ? `${l}-${o}` : `${o}`)
    };
    let s = t;
    Object.keys(r.slots).forEach((_) => {
      if (!r.slots[_] || !(r.slots[_] instanceof Element) && !r.slots[_].el)
        return;
      const a = _.split(".");
      a.forEach((w, v) => {
        s[w] || (s[w] = {}), v !== a.length - 1 && (s = t[w]);
      });
      const p = r.slots[_];
      let u, m, h = !1;
      p instanceof Element ? u = p : (u = p.el, m = p.callback, h = p.clone ?? !1), s[a[a.length - 1]] = u ? m ? (...w) => (m(a[a.length - 1], w), /* @__PURE__ */ g.jsx(y, {
        slot: u,
        clone: h
      })) : /* @__PURE__ */ g.jsx(y, {
        slot: u,
        clone: h
      }) : s[a[a.length - 1]], s = t;
    });
    const i = "children";
    return r[i] && (t[i] = re(r[i], n, `${o}`)), t;
  });
}
function Ze(e, n) {
  return e ? /* @__PURE__ */ g.jsx(y, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function M({
  key: e,
  setSlotParams: n,
  slots: l
}, r) {
  return l[e] ? (...o) => (n(e, o), Ze(l[e], {
    clone: !0,
    ...r
  })) : void 0;
}
function x(e) {
  return U(typeof e == "number" ? e * 1e3 : e);
}
function D(e) {
  return (e == null ? void 0 : e.map((n) => n ? n.valueOf() / 1e3 : null)) || [null, null];
}
const $e = Je(({
  slots: e,
  disabledDate: n,
  value: l,
  defaultValue: r,
  defaultPickerValue: o,
  pickerValue: t,
  presets: s,
  presetItems: i,
  showTime: c,
  onChange: _,
  minDate: a,
  maxDate: p,
  cellRender: u,
  panelRender: m,
  getPopupContainer: h,
  onValueChange: w,
  onPanelChange: v,
  onCalendarChange: I,
  children: S,
  setSlotParams: k,
  elRef: d,
  ...b
}) => {
  const oe = C(n), le = C(h), se = C(u), ce = C(m), ie = E(() => {
    var f;
    return typeof c == "object" ? {
      ...c,
      defaultValue: (f = c.defaultValue) == null ? void 0 : f.map((R) => x(R))
    } : c;
  }, [c]), ae = E(() => l == null ? void 0 : l.map((f) => x(f)), [l]), ue = E(() => r == null ? void 0 : r.map((f) => x(f)), [r]), de = E(() => Array.isArray(o) ? o.map((f) => x(f)) : o ? x(o) : void 0, [o]), fe = E(() => Array.isArray(t) ? t.map((f) => x(f)) : t ? x(t) : void 0, [t]), pe = E(() => a ? x(a) : void 0, [a]), _e = E(() => p ? x(p) : void 0, [p]);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: S
    }), /* @__PURE__ */ g.jsx(ye.RangePicker, {
      ...b,
      ref: d,
      value: ae,
      defaultValue: ue,
      defaultPickerValue: de,
      pickerValue: fe,
      minDate: pe,
      maxDate: _e,
      showTime: ie,
      disabledDate: oe,
      getPopupContainer: le,
      cellRender: e.cellRender ? M({
        slots: e,
        setSlotParams: k,
        key: "cellRender"
      }) : se,
      panelRender: e.panelRender ? M({
        slots: e,
        setSlotParams: k,
        key: "panelRender"
      }) : ce,
      presets: E(() => (s || re(i)).map((f) => ({
        ...f,
        value: D(f.value)
      })), [s, i]),
      onPanelChange: (f, ...R) => {
        const O = D(f);
        v == null || v(O, ...R);
      },
      onChange: (f, ...R) => {
        const O = D(f);
        _ == null || _(O, ...R), w(O);
      },
      onCalendarChange: (f, ...R) => {
        const O = D(f);
        I == null || I(O, ...R);
      },
      renderExtraFooter: e.renderExtraFooter ? M({
        slots: e,
        setSlotParams: k,
        key: "renderExtraFooter"
      }) : b.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ g.jsx(y, {
        slot: e.prevIcon
      }) : b.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ g.jsx(y, {
        slot: e.nextIcon
      }) : b.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ g.jsx(y, {
        slot: e.suffixIcon
      }) : b.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ g.jsx(y, {
        slot: e.superNextIcon
      }) : b.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ g.jsx(y, {
        slot: e.superPrevIcon
      }) : b.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ g.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : b.allowClear,
      separator: e.separator ? /* @__PURE__ */ g.jsx(y, {
        slot: e.separator,
        clone: !0
      }) : b.separator
    })]
  });
});
export {
  $e as DateRangePicker,
  $e as default
};
