import { g as ae, w as S } from "./Index-BWnKV5HS.js";
const E = window.ms_globals.React, se = window.ms_globals.React.forwardRef, G = window.ms_globals.React.useRef, v = window.ms_globals.React.useState, R = window.ms_globals.React.useEffect, ie = window.ms_globals.React.useCallback, q = window.ms_globals.ReactDOM.createPortal, ce = window.ms_globals.antd.theme, ue = window.ms_globals.antd.Spin, de = window.ms_globals.antd.Alert;
var $ = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var fe = E, me = Symbol.for("react.element"), pe = Symbol.for("react.fragment"), _e = Object.prototype.hasOwnProperty, he = fe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ge = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ee(t, e, r) {
  var o, l = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) _e.call(e, o) && !ge.hasOwnProperty(o) && (l[o] = e[o]);
  if (t && t.defaultProps) for (o in e = t.defaultProps, e) l[o] === void 0 && (l[o] = e[o]);
  return {
    $$typeof: me,
    type: t,
    key: n,
    ref: s,
    props: l,
    _owner: he.current
  };
}
O.Fragment = pe;
O.jsx = ee;
O.jsxs = ee;
$.exports = O;
var g = $.exports;
const {
  SvelteComponent: we,
  assign: H,
  binding_callbacks: K,
  check_outros: be,
  children: te,
  claim_element: ne,
  claim_space: ye,
  component_subscribe: V,
  compute_slots: Ee,
  create_slot: xe,
  detach: k,
  element: re,
  empty: J,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: ve,
  get_slot_changes: Ce,
  group_outros: ke,
  init: Ie,
  insert_hydration: P,
  safe_not_equal: Re,
  set_custom_element_data: oe,
  space: Se,
  transition_in: T,
  transition_out: D,
  update_slot_base: Pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Te,
  getContext: Oe,
  onDestroy: Le,
  setContext: je
} = window.__gradio__svelte__internal;
function Z(t) {
  let e, r;
  const o = (
    /*#slots*/
    t[7].default
  ), l = xe(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = re("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      e = ne(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = te(e);
      l && l.l(s), s.forEach(k), this.h();
    },
    h() {
      oe(e, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      P(n, e, s), l && l.m(e, null), t[9](e), r = !0;
    },
    p(n, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && Pe(
        l,
        o,
        n,
        /*$$scope*/
        n[6],
        r ? Ce(
          o,
          /*$$scope*/
          n[6],
          s,
          null
        ) : ve(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (T(l, n), r = !0);
    },
    o(n) {
      D(l, n), r = !1;
    },
    d(n) {
      n && k(e), l && l.d(n), t[9](null);
    }
  };
}
function Fe(t) {
  let e, r, o, l, n = (
    /*$$slots*/
    t[4].default && Z(t)
  );
  return {
    c() {
      e = re("react-portal-target"), r = Se(), n && n.c(), o = J(), this.h();
    },
    l(s) {
      e = ne(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), te(e).forEach(k), r = ye(s), n && n.l(s), o = J(), this.h();
    },
    h() {
      oe(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      P(s, e, a), t[8](e), P(s, r, a), n && n.m(s, a), P(s, o, a), l = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, a), a & /*$$slots*/
      16 && T(n, 1)) : (n = Z(s), n.c(), T(n, 1), n.m(o.parentNode, o)) : n && (ke(), D(n, 1, 1, () => {
        n = null;
      }), be());
    },
    i(s) {
      l || (T(n), l = !0);
    },
    o(s) {
      D(n), l = !1;
    },
    d(s) {
      s && (k(e), k(r), k(o)), t[8](null), n && n.d(s);
    }
  };
}
function Q(t) {
  const {
    svelteInit: e,
    ...r
  } = t;
  return r;
}
function ze(t, e, r) {
  let o, l, {
    $$slots: n = {},
    $$scope: s
  } = e;
  const a = Ee(n);
  let {
    svelteInit: i
  } = e;
  const b = S(Q(e)), d = S();
  V(t, d, (u) => r(0, o = u));
  const m = S();
  V(t, m, (u) => r(1, l = u));
  const c = [], f = Oe("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: w,
    subSlotIndex: _
  } = ae() || {}, y = i({
    parent: f,
    props: b,
    target: d,
    slot: m,
    slotKey: p,
    slotIndex: w,
    subSlotIndex: _,
    onDestroy(u) {
      c.push(u);
    }
  });
  je("$$ms-gr-react-wrapper", y), Te(() => {
    b.set(Q(e));
  }), Le(() => {
    c.forEach((u) => u());
  });
  function h(u) {
    K[u ? "unshift" : "push"](() => {
      o = u, d.set(o);
    });
  }
  function C(u) {
    K[u ? "unshift" : "push"](() => {
      l = u, m.set(l);
    });
  }
  return t.$$set = (u) => {
    r(17, e = H(H({}, e), Y(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, e = Y(e), [o, l, d, m, a, i, s, n, h, C];
}
class Ae extends we {
  constructor(e) {
    super(), Ie(this, e, ze, Fe, Re, {
      svelteInit: 5
    });
  }
}
const X = window.ms_globals.rerender, j = window.ms_globals.tree;
function Ne(t) {
  function e(r) {
    const o = S(), l = new Ae({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: t,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, a = n.parent ?? j;
          return a.nodes = [...a.nodes, s], X({
            createPortal: q,
            node: j
          }), n.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== o), X({
              createPortal: q,
              node: j
            });
          }), s;
        },
        ...r.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
const qe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function De(t) {
  return t ? Object.keys(t).reduce((e, r) => {
    const o = t[r];
    return typeof o == "number" && !qe.includes(r) ? e[r] = o + "px" : e[r] = o, e;
  }, {}) : {};
}
function M(t) {
  const e = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return e.push(q(E.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: E.Children.toArray(t._reactElement.props.children).map((l) => {
        if (E.isValidElement(l) && l.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = M(l.props.el);
          return E.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...E.Children.toArray(l.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(t.getEventListeners()).forEach((l) => {
    t.getEventListeners(l).forEach(({
      listener: s,
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, s, i);
    });
  });
  const o = Array.from(t.childNodes);
  for (let l = 0; l < o.length; l++) {
    const n = o[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = M(n);
      e.push(...a), r.appendChild(s);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Me(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const Ge = se(({
  slot: t,
  clone: e,
  className: r,
  style: o
}, l) => {
  const n = G(), [s, a] = v([]);
  return R(() => {
    var m;
    if (!n.current || !t)
      return;
    let i = t;
    function b() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Me(l, c), r && c.classList.add(...r.split(" ")), o) {
        const f = De(o);
        Object.keys(f).forEach((p) => {
          c.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let c = function() {
        var _, y, h;
        (_ = n.current) != null && _.contains(i) && ((y = n.current) == null || y.removeChild(i));
        const {
          portals: p,
          clonedElement: w
        } = M(t);
        return i = w, a(p), i.style.display = "contents", b(), (h = n.current) == null || h.appendChild(i), p.length > 0;
      };
      c() || (d = new window.MutationObserver(() => {
        c() && (d == null || d.disconnect());
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", b(), (m = n.current) == null || m.appendChild(i);
    return () => {
      var c, f;
      i.style.display = "", (c = n.current) != null && c.contains(i) && ((f = n.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, e, r, o, l]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function We(t, e) {
  return t ? /* @__PURE__ */ g.jsx(Ge, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function F({
  key: t,
  setSlotParams: e,
  slots: r
}, o) {
  return r[t] ? (...l) => (e(t, l), We(r[t], {
    clone: !0,
    ...o
  })) : void 0;
}
function z(t) {
  const e = G(t);
  return e.current = t, ie((...r) => {
    var o;
    return (o = e.current) == null ? void 0 : o.call(e, ...r);
  }, []);
}
function Be(t) {
  const [e, r] = v((t == null ? void 0 : t.eta) ?? null), {
    status: o,
    progress: l,
    queue_position: n,
    message: s,
    queue_size: a
  } = t || {}, [i, b] = v(0), [d, m] = v(0), [c, f] = v(null), [p, w] = v(null), [_, y] = v(null), h = G(!1), C = z(() => {
    requestAnimationFrame(() => {
      m((performance.now() - i) / 1e3), h.current && C();
    });
  }), u = z(() => {
    r(null), f(null), w(null), b(performance.now()), m(0), h.current = !0, C();
  }), I = z(() => {
    m(0), r(null), f(null), w(null), h.current = !1;
  });
  return R(() => {
    o === "pending" ? u() : I();
  }, [u, o, I]), R(() => {
    e === null && r(c), e !== null && c !== e && (w(((performance.now() - i) / 1e3 + e).toFixed(1)), f(e));
  }, [e, c, i]), R(() => {
    y(d.toFixed(1));
  }, [d]), R(() => () => {
    h.current && I();
  }, []), {
    eta: e,
    formattedEta: p,
    formattedTimer: _,
    progress: l,
    queuePosition: n,
    queueSize: a,
    status: o,
    message: s
  };
}
let A = null;
function N(t) {
  const e = ["", "k", "M", "G", "T", "P", "E", "Z"];
  let r = 0;
  for (; t > 1e3 && r < e.length - 1; )
    t /= 1e3, r++;
  const o = e[r];
  return (Number.isInteger(t) ? t : t.toFixed(1)) + o;
}
const He = Ne(({
  slots: t,
  children: e,
  configType: r,
  loadingStatus: o,
  className: l,
  id: n,
  style: s,
  setSlotParams: a,
  showMask: i,
  showTimer: b,
  loadingText: d
}) => {
  var W, B, U;
  let m = null, c = null;
  const {
    status: f,
    message: p,
    progress: w,
    queuePosition: _,
    queueSize: y,
    eta: h,
    formattedEta: C,
    formattedTimer: u
  } = Be(o), I = f === "pending" || f === "generating", le = t.loadingText || typeof d == "string", {
    token: L
  } = ce.useToken();
  if (I)
    if (t.render)
      m = (W = F({
        setSlotParams: a,
        slots: t,
        key: "render"
      })) == null ? void 0 : W(o);
    else
      switch (r) {
        case "antd":
          m = /* @__PURE__ */ g.jsx(ue, {
            size: "small",
            delay: 200,
            style: {
              zIndex: L.zIndexPopupBase,
              backgroundColor: i ? L.colorBgMask : void 0
            },
            tip: le ? t.loadingText ? (B = F({
              setSlotParams: a,
              slots: t,
              key: "loadingText"
            })) == null ? void 0 : B(o) : d : f === "pending" ? /* @__PURE__ */ g.jsxs("div", {
              style: {
                textShadow: "none"
              },
              children: [w ? w.map((x) => /* @__PURE__ */ g.jsx(E.Fragment, {
                children: x.index != null && /* @__PURE__ */ g.jsxs(g.Fragment, {
                  children: [x.length != null ? `${N(x.index || 0)}/${N(x.length)}` : `${N(x.index || 0)}`, x.unit, " "]
                })
              }, x.index)) : _ !== null && y !== void 0 && typeof _ == "number" && _ >= 0 ? `queue: ${_ + 1}/${y} |` : _ === 0 ? "processing |" : null, " ", b && /* @__PURE__ */ g.jsxs(g.Fragment, {
                children: [u, h ? `/${C}` : "", "s"]
              })]
            }) : null,
            className: "ms-gr-auto-loading-default-antd",
            children: /* @__PURE__ */ g.jsx("div", {})
          });
          break;
      }
  if (f === "error" && !A)
    if (t.errorRender)
      c = (U = F({
        setSlotParams: a,
        slots: t,
        key: "errorRender"
      })) == null ? void 0 : U(o);
    else
      switch (r) {
        case "antd":
          A = c = /* @__PURE__ */ g.jsx(de, {
            closable: !0,
            className: "ms-gr-auto-loading-error-default-antd",
            style: {
              zIndex: L.zIndexPopupBase
            },
            message: "Error",
            description: p,
            type: "error",
            onClose: () => {
              A = null;
            }
          });
          break;
      }
  return /* @__PURE__ */ g.jsxs("div", {
    className: l,
    id: n,
    style: s,
    children: [m, c, e]
  });
});
export {
  He as AutoLoading,
  He as default
};
