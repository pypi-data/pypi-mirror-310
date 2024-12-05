import { g as pe, w as S } from "./Index-BvixkM5H.js";
const b = window.ms_globals.React, J = window.ms_globals.React.useMemo, ae = window.ms_globals.React.forwardRef, de = window.ms_globals.React.useRef, ue = window.ms_globals.React.useState, fe = window.ms_globals.React.useEffect, T = window.ms_globals.ReactDOM.createPortal, we = window.ms_globals.antd.Upload;
var Y = {
  exports: {}
}, k = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var me = b, _e = Symbol.for("react.element"), he = Symbol.for("react.fragment"), Ie = Object.prototype.hasOwnProperty, ve = me.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ye = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Q(e, t, r) {
  var s, o = {}, n = null, l = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) Ie.call(t, s) && !ye.hasOwnProperty(s) && (o[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: _e,
    type: e,
    key: n,
    ref: l,
    props: o,
    _owner: ve.current
  };
}
k.Fragment = he;
k.jsx = Q;
k.jsxs = Q;
Y.exports = k;
var X = Y.exports;
const {
  SvelteComponent: be,
  assign: W,
  binding_callbacks: M,
  check_outros: Ee,
  children: Z,
  claim_element: V,
  claim_space: ge,
  component_subscribe: q,
  compute_slots: Re,
  create_slot: xe,
  detach: U,
  element: $,
  empty: z,
  exclude_internal_props: G,
  get_all_dirty_from_scope: Ue,
  get_slot_changes: Se,
  group_outros: Le,
  init: Fe,
  insert_hydration: L,
  safe_not_equal: ke,
  set_custom_element_data: ee,
  space: Oe,
  transition_in: F,
  transition_out: j,
  update_slot_base: Pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ce,
  getContext: Te,
  onDestroy: je,
  setContext: De
} = window.__gradio__svelte__internal;
function H(e) {
  let t, r;
  const s = (
    /*#slots*/
    e[7].default
  ), o = xe(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = $("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = V(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = Z(t);
      o && o.l(l), l.forEach(U), this.h();
    },
    h() {
      ee(t, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      L(n, t, l), o && o.m(t, null), e[9](t), r = !0;
    },
    p(n, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && Pe(
        o,
        s,
        n,
        /*$$scope*/
        n[6],
        r ? Se(
          s,
          /*$$scope*/
          n[6],
          l,
          null
        ) : Ue(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (F(o, n), r = !0);
    },
    o(n) {
      j(o, n), r = !1;
    },
    d(n) {
      n && U(t), o && o.d(n), e[9](null);
    }
  };
}
function Ne(e) {
  let t, r, s, o, n = (
    /*$$slots*/
    e[4].default && H(e)
  );
  return {
    c() {
      t = $("react-portal-target"), r = Oe(), n && n.c(), s = z(), this.h();
    },
    l(l) {
      t = V(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), Z(t).forEach(U), r = ge(l), n && n.l(l), s = z(), this.h();
    },
    h() {
      ee(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      L(l, t, a), e[8](t), L(l, r, a), n && n.m(l, a), L(l, s, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, a), a & /*$$slots*/
      16 && F(n, 1)) : (n = H(l), n.c(), F(n, 1), n.m(s.parentNode, s)) : n && (Le(), j(n, 1, 1, () => {
        n = null;
      }), Ee());
    },
    i(l) {
      o || (F(n), o = !0);
    },
    o(l) {
      j(n), o = !1;
    },
    d(l) {
      l && (U(t), U(r), U(s)), e[8](null), n && n.d(l);
    }
  };
}
function K(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Ae(e, t, r) {
  let s, o, {
    $$slots: n = {},
    $$scope: l
  } = t;
  const a = Re(n);
  let {
    svelteInit: i
  } = t;
  const y = S(K(t)), u = S();
  q(e, u, (d) => r(0, s = d));
  const w = S();
  q(e, w, (d) => r(1, o = d));
  const c = [], m = Te("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: I,
    subSlotIndex: E
  } = pe() || {}, g = i({
    parent: m,
    props: y,
    target: u,
    slot: w,
    slotKey: f,
    slotIndex: I,
    subSlotIndex: E,
    onDestroy(d) {
      c.push(d);
    }
  });
  De("$$ms-gr-react-wrapper", g), Ce(() => {
    y.set(K(t));
  }), je(() => {
    c.forEach((d) => d());
  });
  function p(d) {
    M[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function O(d) {
    M[d ? "unshift" : "push"](() => {
      o = d, w.set(o);
    });
  }
  return e.$$set = (d) => {
    r(17, t = W(W({}, t), G(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, l = d.$$scope);
  }, t = G(t), [s, o, u, w, a, i, l, n, p, O];
}
class We extends be {
  constructor(t) {
    super(), Fe(this, t, Ae, Ne, ke, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, C = window.ms_globals.tree;
function Me(e) {
  function t(r) {
    const s = S(), o = new We({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, a = n.parent ?? C;
          return a.nodes = [...a.nodes, l], B({
            createPortal: T,
            node: C
          }), n.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), B({
              createPortal: T,
              node: C
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
function qe(e) {
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
function h(e) {
  return J(() => qe(e), [e]);
}
const ze = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ge(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const s = e[r];
    return typeof s == "number" && !ze.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function D(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(T(b.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: b.Children.toArray(e._reactElement.props.children).map((o) => {
        if (b.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: l
          } = D(o.props.el);
          return b.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...b.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: l,
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, l, i);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const n = s[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = D(n);
      t.push(...a), r.appendChild(l);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function He(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const Ke = ae(({
  slot: e,
  clone: t,
  className: r,
  style: s
}, o) => {
  const n = de(), [l, a] = ue([]);
  return fe(() => {
    var w;
    if (!n.current || !e)
      return;
    let i = e;
    function y() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), He(o, c), r && c.classList.add(...r.split(" ")), s) {
        const m = Ge(s);
        Object.keys(m).forEach((f) => {
          c.style[f] = m[f];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var E, g, p;
        (E = n.current) != null && E.contains(i) && ((g = n.current) == null || g.removeChild(i));
        const {
          portals: f,
          clonedElement: I
        } = D(e);
        return i = I, a(f), i.style.display = "contents", y(), (p = n.current) == null || p.appendChild(i), f.length > 0;
      };
      c() || (u = new window.MutationObserver(() => {
        c() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", y(), (w = n.current) == null || w.appendChild(i);
    return () => {
      var c, m;
      i.style.display = "", (c = n.current) != null && c.contains(i) && ((m = n.current) == null || m.removeChild(i)), u == null || u.disconnect();
    };
  }, [e, t, r, s, o]), b.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Be(e, t) {
  return e ? /* @__PURE__ */ X.jsx(Ke, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function x({
  key: e,
  setSlotParams: t,
  slots: r
}, s) {
  return r[e] ? (...o) => (t(e, o), Be(r[e], {
    clone: !0,
    ...s
  })) : void 0;
}
function Je(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Qe = Me(({
  slots: e,
  upload: t,
  showUploadList: r,
  progress: s,
  beforeUpload: o,
  customRequest: n,
  previewFile: l,
  isImageUrl: a,
  itemRender: i,
  iconRender: y,
  data: u,
  onChange: w,
  onValueChange: c,
  onRemove: m,
  fileList: f,
  setSlotParams: I,
  ...E
}) => {
  const g = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof r == "object", p = Je(r), O = h(p.showPreviewIcon), d = h(p.showRemoveIcon), te = h(p.showDownloadIcon), N = h(o), ne = h(n), oe = h(s == null ? void 0 : s.format), re = h(l), se = h(a), le = h(i), ie = h(y), ce = h(u), A = J(() => (f == null ? void 0 : f.map((_) => ({
    ..._,
    name: _.orig_name || _.path,
    uid: _.url || _.path,
    status: "done"
  }))) || [], [f]);
  return /* @__PURE__ */ X.jsx(we, {
    ...E,
    fileList: A,
    data: ce || u,
    previewFile: re,
    isImageUrl: se,
    itemRender: e.itemRender ? x({
      slots: e,
      setSlotParams: I,
      key: "itemRender"
    }) : le,
    iconRender: e.iconRender ? x({
      slots: e,
      setSlotParams: I,
      key: "iconRender"
    }) : ie,
    onRemove: (_) => {
      m == null || m(_);
      const P = A.findIndex((v) => v.uid === _.uid), R = f.slice();
      R.splice(P, 1), c == null || c(R), w == null || w(R.map((v) => v.path));
    },
    beforeUpload: async (_, P) => {
      if (N && !await N(_, P))
        return !1;
      const R = (await t([_])).filter((v) => v);
      return c == null || c([...f, ...R]), w == null || w([...f.map((v) => v.path), ...R.map((v) => v.path)]), !1;
    },
    customRequest: ne,
    progress: s && {
      ...s,
      format: oe
    },
    showUploadList: g ? {
      ...p,
      showDownloadIcon: te || p.showDownloadIcon,
      showRemoveIcon: d || p.showRemoveIcon,
      showPreviewIcon: O || p.showPreviewIcon,
      downloadIcon: e["showUploadList.downloadIcon"] ? x({
        slots: e,
        setSlotParams: I,
        key: "showUploadList.downloadIcon"
      }) : p.downloadIcon,
      removeIcon: e["showUploadList.removeIcon"] ? x({
        slots: e,
        setSlotParams: I,
        key: "showUploadList.removeIcon"
      }) : p.removeIcon,
      previewIcon: e["showUploadList.previewIcon"] ? x({
        slots: e,
        setSlotParams: I,
        key: "showUploadList.previewIcon"
      }) : p.previewIcon,
      extra: e["showUploadList.extra"] ? x({
        slots: e,
        setSlotParams: I,
        key: "showUploadList.extra"
      }) : p.extra
    } : r
  });
});
export {
  Qe as Upload,
  Qe as default
};
