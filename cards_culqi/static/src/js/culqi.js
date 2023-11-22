/*
 *   Copyright (c) 2020 
 *   All rights reserved.
 */
/*
 *   Jhon Alexander Grisales Rivera
 *   Copyright (c) 2020 
 *   All rights reserved.
 */

var odoo_order_id = null;
var odoo_order = null;
var odoo_order_customer = null;
var culqi_enviroment = null;
var checkout_items = null;
var _acquirer_id = null;
var global_amount_total = null;

odoo.define('module.CQ', function(require) 
{
    "use strict";
    var rpc = require('web.rpc');
    var dialog = require('web.Dialog');

    $(document).ready(function() 
    {
        var url_string = window.location.href;
        var url = new URL(url_string);
        var state = url.searchParams.get("state");
        var message = url.searchParams.get("message");
        if (state == "done" || state == "venta_exitosa")
        {
            $('.o_wsale_my_cart').fadeOut();
            /*
            swal({
                    title: "Orden de Venta",
                    text: message,
                    type: "success",
                    showCancelButton: true,
                    cancelButtonText: "OK",
                    closeOnCancel: true
                });
            */
            dialog.alert(null, String(message));
        }
        else
        {
            if(String(state)!= String("null"))
            {
                /*
                swal({
                        title: "Solicitud Orden de Venta",
                        text: message,
                        type: "warning",
                        showCancelButton: true,
                        cancelButtonText: "OK",
                        closeOnCancel: true
                    });
                */
                dialog.alert(null, String('Solicitud Orden de Venta'));
            }
            
        }
        
        var default_button = $("form.o_payment_form").find("button#o_payment_form_pay");

        if ($("#payment_method").length > 0) {
            $("#o_payment_form_pay").after(function() {
                initCulqiPagoAcquirer();    
            });
        }
        
        $("button#o_payment_form_pay").on("click",function()
        {
            event.preventDefault();
            var data_provider = $("input[name='pm_id']:checked").attr("data-provider");
            if(data_provider=="culqi")
            {
                Culqi.open();
                event.preventDefault();
                
                setInterval(function()
                {
                    $("button#o_payment_form_pay").find("span.o_loader").remove();
                    $("button#o_payment_form_pay").removeAttr("disabled");
                }, 1);
                
            }     
            else{
                if(data_provider!="culqi")
                    $("form.o_payment_form").submit();
            }       
        });
        
    });

    function initCulqiPagoAcquirer()
    {
        var data = { "params": {  } }
        $.ajax({
                    type: "POST",
                    url: '/culqi/get_culqi_acquirer',
                    data: JSON.stringify(data),
                    dataType: 'json',
                    contentType: "application/json",
                    async: false,
                    success: function(response) 
                    {
                        var acquirer = response.result.acquirer;
                        if(String(acquirer.state)=="enabled" || String(acquirer.state)=="test")
                        {                        
                            createPreference(acquirer, Culqi)
                        }                 
                    }
                });
    }
    
    function createPreference(acquirer, Culqi)
    {
        var partner_id = $(".o_payment_form").attr("data-partner-id");
        var acquirer_id = $('input[data-provider="culqi"]').attr("data-acquirer-id");
        var online_payment = "no";

        if($("#quote_content").length>0)
        {
            online_payment = "yes";
        }

        var data = { "params": { partner_id: partner_id, acquirer_id: acquirer_id , online_payment: online_payment } }

        $.ajax({
            type: "POST",
            url: '/culqi/get_sale_order',
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: "application/json",
            async: false,
            success: function(response) 
            {
                var json_preference = response.result.json_preference;
                var preference = json_preference
                var state_enviroment = response.result.environment;
                var product_lines = response.result.product_lines;
                var customer = response.result.customer;
                var currency_name = response.result.currency_name;

                global_amount_total = preference.amount_total
                var amount = parseInt(String(String(parseFloat(preference.amount_total).toFixed(2)).replace(".","")).replace(",",""));

                if(state_enviroment=='test')
                {                                        
                    culqi_enviroment = 'sandbox'  
                    Culqi.publicKey = acquirer.culqi_public_key;                  
                }

                if(state_enviroment=='enabled')
                {                    
                    culqi_enviroment = 'production'
                    Culqi.publicKey = acquirer.culqi_public_key_produccion;
                } 
                var culqi_transaction = {
                                            title: preference.name,
                                            currency: currency_name,
                                            description: product_lines,
                                            amount: amount
                                        }
                odoo_order = culqi_transaction;
                odoo_order_id = preference.id;
                odoo_order_customer = customer;
                checkout_items = response.result.checkout_items;
                _acquirer_id = acquirer_id;

                Culqi.settings(culqi_transaction);               
            }
        });
    }
});
/**
 * This function should be rigth listener 
 * but it isen't getting token or some error
 * 
 * Main file was loaded locally but not properlly as 
 * docummentation recommends. Anyway working with Odoo
 */
 function culqi() {
    if (Culqi.token) {
      // Objeto Token creado exitosamente!
      const token = Culqi.token.id;
      console.log("Se ha creado un Token: ", token);
      handleCulqiToken(token);
    } else if (Culqi.order) {
      // Objeto order creado exitosamente!
      const order = Culqi.order;
      console.log("Se ha creado el objeto Order: ", order);
      if (order.paymentCode) {
        console.log("Se ha creado el cip: ", order.paymentCode);
      }
      if (order.qr) {
        console.log("Se ha generado el qr: ", order.qr);
      }
      if (order.cuotealo) {
        console.log("Se ha creado el link cuotéalo: ", order.cuotealo);
      }
    } else {
      // Mostramos JSON de objeto error en consola
      console.log("Error : ", Culqi.error);
    }
  }

function handleCulqiToken(token)
{
    //alert(token)    
    if(String(token).length > 0)
    {
        //alert(global_amount_total)
        var data = { "params": { 
                                    'enviroment':culqi_enviroment, 
                                    'token': token, 
                                    'culqi_preference': odoo_order, 
                                    'customer': odoo_order_customer, 
                                    'odoo_order_id':odoo_order_id , 
                                    'checkout_items':checkout_items,
                                    'acquirer_id':_acquirer_id,
                                    'amount_total':global_amount_total
                                } 
                    }
        $.ajax({
            type: "POST",
            url: '/culqi/process_culqi_payment',
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: "application/json",
            async: false,
            success: function(response) 
            {   
                console.log(response)
                var url_send = response.result.url_send;
                window.location = url_send
            }
        });
    }
}

window.culqijs = function(I) {
    var c = {};

    function u(l) {
        if (c[l]) return c[l].exports;
        var s = c[l] = {
            i: l,
            l: !1,
            exports: {}
        };
        return I[l].call(s.exports, s, s.exports, u), s.l = !0, s.exports
    }
    return u.m = I, u.c = c, u.d = function(l, s, b) {
        u.o(l, s) || Object.defineProperty(l, s, {
            enumerable: !0,
            get: b
        })
    }, u.r = function(l) {
        typeof Symbol < "u" && Symbol.toStringTag && Object.defineProperty(l, Symbol.toStringTag, {
            value: "Module"
        }), Object.defineProperty(l, "__esModule", {
            value: !0
        })
    }, u.t = function(l, s) {
        if (1 & s && (l = u(l)), 8 & s || 4 & s && typeof l == "object" && l && l.__esModule) return l;
        var b = Object.create(null);
        if (u.r(b), Object.defineProperty(b, "default", {
                enumerable: !0,
                value: l
            }), 2 & s && typeof l != "string")
            for (var f in l) u.d(b, f, function(d) {
                return l[d]
            }.bind(null, f));
        return b
    }, u.n = function(l) {
        var s = l && l.__esModule ? function() {
            return l.default
        } : function() {
            return l
        };
        return u.d(s, "a", s), s
    }, u.o = function(l, s) {
        return Object.prototype.hasOwnProperty.call(l, s)
    }, u.p = "", u(u.s = 0)
}([function(I, c, u) {
    "use strict";
    Object.defineProperty(c, "__esModule", {
        value: !0
    }), Object.defineProperty(c, "Checkout", {
        enumerable: !0,
        get: function() {
            return l.default
        }
    }), Object.defineProperty(c, "Elements", {
        enumerable: !0,
        get: function() {
            return s.default
        }
    });
    var l = b(u(1)),
        s = b(u(2));

    function b(f) {
        return f && f.__esModule ? f : {
            default: f
        }
    }
}, function(I, c, u) {
    "use strict";

    function l(o, v) {
        for (var k = 0; k < v.length; k++) {
            var r = v[k];
            r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(o, r.key, r)
        }
    }
    Object.defineProperty(c, "__esModule", {
        value: !0
    }), c.default = void 0;
    var s, b = !1,
        f, d, p, g, x = !1,
        e, E, n = {
            lang: "auto",
            modal: !0,
            installments: !1,
            paymentMethods: {
                tarjeta: 0,
                bancaMovil: 0,
                agente: 0,
                billetera: 0,
                cuotealo: 0,
                yape: 0
            },
            style: {
                bannerColor: "",
                buttonBackground: "",
                menuColor: "",
                linksColor: "",
                buttontext: "",
                priceColor: "",
                logo: ""
            }
        },
        m = "",
        y = "",
        S = function() {
            function o() {
                (function(t, a) {
                    if (!(t instanceof a)) throw new TypeError("Cannot call a class as a function")
                })(this, o)
            }
            var v, k, r;
            return v = o, (k = [{
                key: "_cambiarContenedor",
                value: function() {
                    return m == "" ? "document.body" : m
                }
            }, {
                key: "init",
                value: function() {
                    console.log("%cCULQI JS%cv4", "padding: 5px; border-radius: 4px 0 0 4px; background: linear-gradient(#34c4ad, #0AA6A9); color: #FFF; text-transform: uppercase; font-size: 10px;font-family: sans-serif;font-weight: bold;text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.3)", "padding: 5px; border-radius: 0 4px 4px 0; background-color: #676767; color: #FFF; text-transform: uppercase; font-size: 10px;font-family: sans-serif")
                }
            }, {
                key: "initCheckout",
                value: function(t) {
                    C(t)
                }
            }, {
                key: "settings",
                value: function(t) {
                    var a = !0;
                    return y.length > 5 ? (e = t, Number(e.amount) % 1 == 0 ? (e.amount = Number(e.amount), window.addEventListener("message", q, !1), this.initCheckout(!0), a = !0) : (window.addEventListener("message", q, !1), this.initCheckout(!0), a = !0)) : (x || console.log("%cJS%cNo configuro publicKey", "padding: 5px; border-radius: 4px 0 0 4px; background-color: #38d9a9; color: #222b31; text-transform: uppercase; font-weight: bold; font-size: 10px;font-family: sans-serif", "padding: 5px; border-radius: 0 4px 4px 0; background-color: #ad1411; color: #FFF; text-transform: uppercase; font-size: 10px;font-family: sans-serif; font-weight: bold; text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.3)"), a = !1), a
                }
            }, {
                key: "options",
                value: function(t) {
                    const a = _ => typeof _ == "boolean" && _ === !0;
                    return t !== void 0 && (t.lang !== void 0 && (n.lang = t.lang), t.modal !== void 0 && (n.modal = t.modal), t.head !== void 0 && (n.head = t.head), t.head !== void 0 && (n.head = t.head), t.installments !== void 0 && t.installments != "" && (n.installments = t.installments), t.paymentMethods !== void 0 && (t.paymentMethods.tarjeta !== void 0 && (n.paymentMethods.tarjeta = a(t.paymentMethods.tarjeta)), t.paymentMethods.bancaMovil !== void 0 && (n.paymentMethods.bancaMovil = a(t.paymentMethods.bancaMovil)), t.paymentMethods.agente !== void 0 && (n.paymentMethods.agente = a(t.paymentMethods.agente)), t.paymentMethods.yape !== void 0 && (n.paymentMethods.yape = a(t.paymentMethods.yape)), t.paymentMethods.billetera !== void 0 && (n.paymentMethods.billetera = a(t.paymentMethods.billetera)), t.paymentMethods.cuotealo !== void 0 && (n.paymentMethods.cuotealo = a(t.paymentMethods.cuotealo))), t.style !== void 0 && (t.style.bannerColor !== void 0 && (n.style.bannerColor = t.style.bannerColor), t.style.buttonBackground !== void 0 && (n.style.buttonBackground = t.style.buttonBackground), t.style.menuColor !== void 0 && (n.style.menuColor = t.style.menuColor), t.style.linksColor !== void 0 && (n.style.linksColor = t.style.linksColor), t.style.buttonText !== void 0 && (n.style.buttonText = t.style.buttonText), t.style.buttonTextColor !== void 0 && (n.style.buttonTextColor = t.style.buttonTextColor), t.style.priceColor !== void 0 && (n.style.priceColor = t.style.priceColor), t.style.logo !== void 0 && (n.style.logo = t.style.logo))), n
                }
            }, {
                key: "open",
                value: function() {
                    w()
                }
            }, {
                key: "close",
                value: function() {
                    C(!0)
                }
            }, {
                key: "validationPaymentMethods",
                value: function() {
                    var t = n.paymentMethods,
                        a = {},
                        _ = y.includes("pk_live_") ? "live" : y.includes("pk_test_") ? "test" : null;

                    function A(M, R) {
                        var O = {
                                order_id: R,
                                order_types: [M]
                            },
                            B = JSON.stringify(O),
                            i = new XMLHttpRequest;
                        p = void 0, i.open("POST", "https://api.culqi.com/v2/orders/confirm", !0), i.setRequestHeader("Content-type", "application/json"), i.setRequestHeader("Authorization", "Bearer " + y), i.setRequestHeader("X-API-KEY", y), i.setRequestHeader("X-CULQI-CLIENT", "culqiJS_v4"), i.setRequestHeader("X-CULQI-SPONSOR", e.culqiclient ? e.culqiclient : ""), i.setRequestHeader("X-CULQI-SPONSOR-VERSION", e.culqiclientversion ? e.culqiclientversion : ""), i.setRequestHeader("X-CULQI-PRODUCT", "online"), i.onreadystatechange = function() {
                            return i.status == 200 || i.status == 201 ? (i.readyState == 4 && (s = JSON.parse(i.response), culqi()), !1) : (i.readyState == 4 && (p = JSON.parse(i.response), culqi()), !1)
                        }, i.send(B)
                    }

                    function N() {
                        var M, R, O, B, i;
                        M = document.getElementsByClassName("culqi-email").length > 0 ? document.getElementsByClassName("culqi-email")[0] : document.querySelectorAll('[data-culqi="card[email]"]').length > 0 ? document.querySelectorAll('[data-culqi="card[email]"]')[0] : document.getElementById("card[email]"), R = document.getElementsByClassName("culqi-card").length > 0 ? document.getElementsByClassName("culqi-card")[0] : document.querySelectorAll('[data-culqi="card[number]"]').length > 0 ? document.querySelectorAll('[data-culqi="card[number]"]')[0] : document.getElementById("card[number]"), O = document.getElementsByClassName("culqi-cvv").length > 0 ? document.getElementsByClassName("culqi-cvv")[0] : document.querySelectorAll('[data-culqi="card[cvv]"]').length > 0 ? document.querySelectorAll('[data-culqi="card[cvv]"]')[0] : document.getElementById("card[cvv]"), B = document.getElementsByClassName("culqi-expy").length > 0 ? document.getElementsByClassName("culqi-expy")[0] : document.querySelectorAll('[data-culqi="card[exp_year]"]').length > 0 ? document.querySelectorAll('[data-culqi="card[exp_year]"]')[0] : document.getElementById("card[exp_year]"), i = document.getElementsByClassName("culqi-expm").length > 0 ? document.getElementsByClassName("culqi-expm")[0] : document.querySelectorAll('[data-culqi="card[exp_month]"]').length > 0 ? document.querySelectorAll('[data-culqi="card[exp_month]"]')[0] : document.getElementById("card[exp_month]");
                        var j = {
                                email: M.value,
                                card_number: R.value.replace(/\s/g, ""),
                                cvv: O.value,
                                expiration_year: B.value,
                                expiration_month: i.value
                            },
                            F = JSON.stringify(j),
                            h = new XMLHttpRequest;
                        p = void 0, h.open("POST", "https://secure.culqi.com/tokens", !0), h.setRequestHeader("Content-type", "application/json"), h.setRequestHeader("Authorization", "Bearer " + y), h.setRequestHeader("X-API-VERSION", "2"), h.setRequestHeader("X-API-KEY", y), h.setRequestHeader("X-CULQI-ENV", _), h.setRequestHeader("X-CULQI-CLIENT", "culqiJS_v4"), h.setRequestHeader("X-CULQI-SPONSOR", e.culqiclient ? e.culqiclient : ""), h.setRequestHeader("X-CULQI-SPONSOR-VERSION", e.culqiclientversion ? e.culqiclientversion : ""), h.setRequestHeader("X-CULQI-PRODUCT", "online"), h.onreadystatechange = function() {
                            return h.status == 200 || h.status == 201 ? (h.readyState == 4 && (d = JSON.parse(h.response), culqi()), !1) : (h.readyState == 4 && (p = JSON.parse(h.response), culqi()), !1)
                        }, h.send(F)
                    }

                    function P() {
                        var M, R;
                        M = document.getElementsByClassName("culqi-phone").length > 0 ? document.getElementsByClassName("culqi-phone")[0] : document.querySelectorAll('[data-culqi="yape[phone]"]').length > 0 ? document.querySelectorAll('[data-culqi="yape[phone]"]')[0] : document.getElementById("yape[phone]"), R = document.getElementsByClassName("culqi-code").length > 0 ? document.getElementsByClassName("culqi-code")[0] : document.querySelectorAll('[data-culqi="yape[code]"]').length > 0 ? document.querySelectorAll('[data-culqi="yape[code]"]')[0] : document.getElementById("yape[code]");
                        var O = {
                                number_phone: M.value.replace(/\s/g, ""),
                                otp: R.value,
                                amount: e.amount
                            },
                            B = JSON.stringify(O),
                            i = new XMLHttpRequest;
                        p = void 0, i.open("POST", "https://secure.culqi.com/v2/tokens/yape", !0), i.setRequestHeader("Content-type", "application/json"), i.setRequestHeader("Authorization", "Bearer " + y), i.setRequestHeader("X-API-KEY", y), i.setRequestHeader("X-CULQI-CLIENT", "culqiJS_v4"), i.setRequestHeader("X-CULQI-SPONSOR", e.culqiclient ? e.culqiclient : ""), i.setRequestHeader("X-CULQI-SPONSOR-VERSION", e.culqiclientversion ? e.culqiclientversion : ""), i.setRequestHeader("X-CULQI-PRODUCT", "online"), i.onreadystatechange = function() {
                            return i.status == 200 || i.status == 201 ? (i.readyState == 4 && (d = JSON.parse(i.response), culqi()), !1) : (i.readyState == 4 && (p = JSON.parse(i.response), culqi()), !1)
                        }, i.send(B)
                    }
                    typeof t.tarjeta == "boolean" ? t.tarjeta ? e.amount ? e.amount < 300 ? a.token = {
                        available: !1,
                        message: "El monto ingresado debe ser mayor a S/3"
                    } : isNaN(e.amount) ? a.token = {
                        available: !1,
                        message: "Tiene que ingresar solo n\xFAmeros enteros"
                    } : a.token = {
                        available: !0,
                        generate: function() {
                            N()
                        }
                    } : a.token = {
                        available: !1,
                        message: "Debe ingresar el monto en el campo 'amount'"
                    } : a.token = {
                        available: !1,
                        message: "No habilitado"
                    } : a.token = {
                        available: !1,
                        message: "El valor ingresado debe ser tipo boolean"
                    }, typeof t.yape == "boolean" ? t.yape ? !e.amount && !e.currency ? a.yape = {
                        available: !1,
                        message: "Debe ingresar el monto en el campo 'amount' y el tipo de moneda en el campo 'currency'"
                    } : e.amount && !e.currency ? a.yape = {
                        available: !1,
                        message: "Debe ingresar el tipo de moneda en el campo 'currency'. Esta opci\xF3n solo est\xE1 habilitado para 'PEN'"
                    } : !e.amount && e.currency ? a.yape = {
                        available: !1,
                        message: "Debe ingresar el monto en el campo 'amount'"
                    } : e.currency === "PEN" ? e.amount >= 300 ? a.yape = {
                        available: !0,
                        generate: function() {
                            P()
                        }
                    } : a.yape = {
                        available: !1,
                        message: "Monto no v\xE1lido, m\xEDnimo S/ 3.00"
                    } : a.yape = {
                        available: !1,
                        message: "Actualmente esta opci\xF3n solo est\xE1 habilitado para 'PEN'"
                    } : a.yape = {
                        available: !1,
                        message: "No habilitado"
                    } : a.yape = {
                        available: !1,
                        message: "El valor ingresado debe ser tipo boolean"
                    }, e.order === "" || e.order === void 0 ? (a.cip = {
                        available: !1,
                        message: "Debe ingresar el order"
                    }, a.cuotealo = {
                        available: !1,
                        message: "Debe ingresar el order"
                    }) : (typeof t.agente == "boolean" || typeof t.billetera == "boolean" || typeof t.bancaMovil == "boolean" ? t.agente || t.billetera || t.bancaMovil ? !e.amount && !e.currency ? (a.cip = {
                        available: !1,
                        message: "Debe ingresar el monto en el campo 'amount' y el tipo de moneda en el campo 'currency'"
                    }, a.cuotealo = {
                        available: !1,
                        message: "Debe ingresar el monto en el campo 'amount' y el tipo de moneda en el campo 'currency'"
                    }) : e.amount && !e.currency ? (a.cip = {
                        available: !1,
                        message: "Debe ingresar el tipo de moneda en el campo 'currency'"
                    }, a.cuotealo = {
                        available: !1,
                        message: "Debe ingresar el tipo de moneda en el campo 'currency'"
                    }) : !e.amount && e.currency ? (a.cip = {
                        available: !1,
                        message: "Debe ingresar el monto en el campo 'amount'"
                    }, a.cuotealo = {
                        available: !1,
                        message: "Debe ingresar el monto en el campo 'amount'"
                    }) : (e.currency === "PEN" && (e.amount >= 600 && e.amount <= 2e6 ? a.cip = {
                        available: !0,
                        generate: function() {
                            A("cip", e.order)
                        }
                    } : a.cip = {
                        available: !1,
                        message: "Monto no v\xE1lido, m\xEDnimo S/6 y m\xE1ximo S/20,000"
                    }), e.currency === "USD" && (e.amount >= 600 && e.amount <= 2e6 ? a.cip = {
                        available: !0,
                        generate: function() {
                            A("cip", e.order)
                        }
                    } : a.cip = {
                        available: !1,
                        message: "Monto no v\xE1lido, m\xEDnimo $6 y m\xE1ximo $20,000"
                    })) : a.cip = {
                        available: !1,
                        message: "No habilitado"
                    } : a.cip = {
                        available: !1,
                        message: "El valor ingresado debe ser tipo boolean"
                    }, typeof t.cuotealo == "boolean" ? t.cuotealo ? !e.amount && !e.currency ? (a.cip = {
                        available: !1,
                        message: "Debe ingresar el monto en el campo 'amount' y el tipo de moneda en el campo 'currency'"
                    }, a.cuotealo = {
                        available: !1,
                        message: "Debe ingresar el monto en el campo 'amount' y el tipo de moneda en el campo 'currency'"
                    }) : e.amount && !e.currency ? (a.cip = {
                        available: !1,
                        message: "Debe ingresar el tipo de moneda en el campo 'currency'"
                    }, a.cuotealo = {
                        available: !1,
                        message: "Debe ingresar el tipo de moneda en el campo 'currency'"
                    }) : !e.amount && e.currency ? (a.cip = {
                        available: !1,
                        message: "Debe ingresar el monto en el campo 'amount'"
                    }, a.cuotealo = {
                        available: !1,
                        message: "Debe ingresar el monto en el campo 'amount'"
                    }) : (e.currency === "USD" && (e.amount >= 3e3 && e.amount <= 2e5 ? a.cuotealo = {
                        available: !0,
                        generate: function() {
                            A("cuotealo", e.order)
                        }
                    } : a.cuotealo = {
                        available: !1,
                        message: "Monto no v\xE1lido, m\xEDnimo $30 y m\xE1ximo $2,000"
                    }), e.currency === "PEN" && (e.amount >= 1e4 && e.amount <= 7e5 ? a.cuotealo = {
                        available: !0,
                        generate: function() {
                            A("cuotealo", e.order)
                        }
                    } : a.cuotealo = {
                        available: !1,
                        message: "Monto no v\xE1lido, m\xEDnimo S/100 y m\xE1ximo S/7,000"
                    })) : a.cuotealo = {
                        available: !1,
                        message: "No habilitado"
                    } : a.cuotealo = {
                        available: !1,
                        message: "El valor ingresado debe ser tipo boolean"
                    }), E = a
                }
            }, {
                key: "env",
                set: function(t) {
                    x = t
                }
            }, {
                key: "name",
                get: function() {
                    return "Culqi Checkout v4.0"
                }
            }, {
                key: "isOpen",
                get: function() {
                    return b
                }
            }, {
                key: "publicKey",
                get: function() {
                    return y
                },
                set: function(t) {
                    y = t
                }
            }, {
                key: "paymentOptionsAvailable",
                get: function() {
                    return E
                }
            }, {
                key: "container",
                get: function() {
                    return m
                },
                set: function(t) {
                    m = t
                }
            }, {
                key: "getSettings",
                get: function() {
                    return e
                }
            }, {
                key: "getOptions",
                get: function() {
                    return n
                }
            }, {
                key: "order",
                get: function() {
                    return s
                }
            }, {
                key: "token",
                get: function() {
                    return d
                },
                set: function(t) {
                    d = t
                }
            }, {
                key: "error",
                get: function() {
                    return p
                }
            }, {
                key: "closeEvent",
                get: function() {
                    return g
                }
            }]) && l(v.prototype, k), r && l(v, r), o
        }();

    function w() {
        b = !0;
        var o;
        navigator.vendor == "Apple Computer, Inc." && altScrollTo.call(window, 0, 0), document.querySelector(".culqi_checkout") != null && ((o = document.getElementById("culqi_checkout_frame")).style.visibility = "visible", o.style.display = "block", o.style.width = "100%", o.style.height = "100%")
    }

    function C(o, v) {
        b = !1;
        var k, r = null,
            t = null,
            a = "?public_key=" + y + "&title=" + encodeURIComponent(window.btoa(unescape(encodeURIComponent(e.title)))) + "&currency=" + encodeURIComponent(window.btoa(unescape(encodeURIComponent(e.currency)))) + "&description=" + encodeURIComponent(window.btoa(unescape(encodeURIComponent(e.description)))) + "&amount=" + encodeURIComponent(window.btoa(unescape(encodeURIComponent(e.amount)))) + "&logo=" + encodeURIComponent(window.btoa(unescape(encodeURIComponent(n.style.logo)))) + "&installments=" + n.installments + "&monto=" + (isNaN(e.amount) ? !1 : e.amount > 0) + "&version=4";
        if (e.order !== void 0 ? a += "&orders=" + encodeURIComponent(window.btoa(unescape(encodeURIComponent(e.order)))) : a += "&orders=", document.querySelector(".culqi_checkout") == null) {
            (r = document.createElement("IFRAME")).setAttribute("src", "https://checkout.culqi.com/v4" + a), r.setAttribute("id", "culqi_checkout_frame"), r.setAttribute("name", "checkout_frame"), r.setAttribute("class", "culqi_checkout"), r.setAttribute("allowtransparency", "true"), r.setAttribute("frameborder", "0"), r.style.backgroundColor = "rgba(0,0,0,0.62)", r.style.border = "0px none trasparent", r.style.overflowX = "hidden", r.style.overflowY = "auto", r.style.margin = "0px", n.modal ? (r.style.zIndex = 99999, r.style.position = "fixed", r.style.visibility = "hidden", r.style.visibility = "collapse", r.style.height = 0, r.style.width = 0) : (r.setAttribute("frameborder", 0), r.setAttribute("allowfullscreen", !0), r.style.height = "100%", r.style.width = "100%"), r.style.left = "0px", r.style.top = "0px", r.style.backgroundPosition = "initial initial", r.style.backgroundRepeat = "initial initial", k = m != "" ? document.getElementById(m) : document.body;
            try {
                k.appendChild(r)
            } catch (_) {
                console.log("%c>JS> Error: No existe contenedor %c" + k + "%c" + _, "padding: 0 10px; background-color: #000000; color: #ff0000; text-transform: uppercase; font-weight: bold;", "background-color: #000000; padding: 0 10px; color: #fff", "padding: 0 10px; color: #ff0000; font-weight: bold;")
            }
            navigator.vendor == "Apple Computer, Inc." && (window.altScrollTo = r.contentWindow.scrollTo), (t = document.getElementById("culqi_checkout_frame")).addEventListener("load", function() {
                (function(_) {
                    _ === !0 && console.log("%cCULQI Checkout%cv4.0", "padding: 5px; border-radius: 4px 0 0 4px; background: linear-gradient(#34c4ad, #0AA6A9); color: #FFF; text-transform: uppercase; font-size: 10px;font-family: sans-serif;font-weight: bold;text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.3)", "padding: 5px; border-radius: 0 4px 4px 0; background-color: #676767; color: #FFF; text-transform: uppercase; font-size: 10px;font-family: sans-serif")
                })(o),
                function() {
                    var _ = S,
                        A = {
                            _publicKey: y,
                            _settings: e,
                            _options: n
                        },
                        N = document.getElementById("culqi_checkout_frame");
                    N ? N.contentWindow.postMessage(A, "*") : console.log("%c>JS> Error: Revise contenedor %c" + _.container, "padding: 0 10px; background-color: #000000; color: #ff0000; text-transform: uppercase; font-weight: bold;", "background-color: #000000; padding: 0 10px 0 0; color: #fff")
                }(), o || v === void 0 || (t.contentWindow.postMessage({
                    type: "recupera",
                    data: v,
                    order: f
                }, "*"), w())
            })
        } else(t = document.getElementById("culqi_checkout_frame")) != null && (t.parentNode.removeChild(t), C(!1, v));
        return !0
    }

    function q(o) {
        var v, k;
        if (g = null, typeof o.data == "string") try {
            v = JSON.parse(o.data)
        } catch {
            switch (o.data) {
                case "culqi_destroy_checkout":
                    setTimeout(function() {
                        document.getElementById("culqi_checkout_frame").remove()
                    }, 500);
                    break;
                case "checkout_cerrado":
                    b = !1, g = o.data, d = null, (k = document.getElementById("culqi_checkout_frame")) != null && (k.style.visibility = "hidden", k.style.visibility = "collapse", k.style.width = "10px", k.style.height = "0px");
                    break;
                case "checkout_cargando_recupera":
                    g = o.data, d = null, culqi();
                    break;
                default:
                    o.data != "" && console.log("%cJS%cNo se reconoce Instrucci\xF3n%c" + o.data, "padding: 5px; border-radius: 4px 0 0 4px; background-color: #38d9a9; color: #222b31; text-transform: uppercase; font-size: 10px;font-family: sans-serif", "padding: 5px; background-color: #222b31; color: #ff8f00; text-transform: uppercase; font-size: 10px;font-family: sans-serif;border-left: 5px solid #ff8f00;", "padding: 5px; border-radius: 0 4px 4px 0; background-color: #08696b; color: #fff; text-transform: uppercase; font-size: 10px;font-family: sans-serif; font-weight: bold;text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.3)")
            }
        } else if (typeof o.data < "u" && typeof o.data.object == "string") switch (o.data.object) {
            case "error":
                var r = o.data.type ? o.data.type.replace(/_/g, " ") : "Error",
                    t = o.data.param ? o.data.param : "",
                    a = o.data.merchant_message ? o.data.merchant_message : "",
                    _ = o.data.user_message ? o.data.user_message : "";
                console.log("%cJS%c" + r + "%c" + t + "%c" + a + ": " + _, "padding: 5px; border-radius: 4px 0 0 4px; background-color: #38d9a9; color: #222b31; text-transform: uppercase; font-size: 10px;font-family: sans-serif", "padding: 5px; background-color: #222b31; color: #ff4f4f; text-transform: uppercase; font-size: 10px;font-family: sans-serif;border-left: 5px solid #ff4f4f;", "padding: 5px; border-radius: 0 4px 4px 0; background-color: #08696b; color: #fff; text-transform: uppercase; font-size: 10px;font-family: sans-serif; font-weight: bold;text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.3)", "color: #FFF; font-family: sans-serif");
                var A = function() {
                    var N = navigator.userAgent.toLowerCase();
                    return N.indexOf("msie") != -1 && parseInt(N.split("msie")[1])
                };
                v = A() && A() < 9 ? JSON.parse(o.data) : o.data, p = v, e.version != "2" && culqi(), e.order, d = null, f = null, s = null;
                break;
            case "order":
                s = o.data, p = null, d = null, culqi();
                break;
            case "token":
                console.log("%cJS%c" + o.data.object + "%c" + o.data.id, "padding: 5px; border-radius: 4px 0 0 4px; background-color: #38d9a9; color: #222b31; text-transform: uppercase; font-size: 10px;font-family: sans-serif", "padding: 5px; background-color: #222b31; color: #ff8f00; text-transform: uppercase; font-size: 10px;font-family: sans-serif;border-left: 5px solid #ff8f00;", "padding: 5px; border-radius: 0 4px 4px 0; background-color: #08696b; color: #fff; text-transform: uppercase; font-size: 10px;font-family: sans-serif; font-weight: bold;text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.3)"), d = o.data, p = null, f = Object.assign({}, s), s = null, culqi()
        }
    }
    c.default = S, I.exports = c.default
}, function(I, c, u) {
    "use strict";
    Object.defineProperty(c, "__esModule", {
        value: !0
    }), c.default = void 0;
    var l, s = (l = u(3)) && l.__esModule ? l : {
        default: l
    };

    function b(n) {
        return (b = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(m) {
            return typeof m
        } : function(m) {
            return m && typeof Symbol == "function" && m.constructor === Symbol && m !== Symbol.prototype ? "symbol" : typeof m
        })(n)
    }

    function f(n, m) {
        for (var y = 0; y < m.length; y++) {
            var S = m[y];
            S.enumerable = S.enumerable || !1, S.configurable = !0, "value" in S && (S.writable = !0), Object.defineProperty(n, S.key, S)
        }
    }
    var d, p, g = "",
        x = "https://checkout.culqi.com/v4/#/elements",
        e = x + "/controller/",
        E = function() {
            function n(w) {
                (function(C, q) {
                    if (!(C instanceof q)) throw new TypeError("Cannot call a class as a function")
                })(this, n), this.iframe = document.createElement("IFRAME"), this.elementStatus = "init", w ? (g = w, console.log("%cCULQI Elements%c", "padding: 5px; border-radius: 4px 0 0 4px; background: linear-gradient(#34c4ad, #0AA6A9); color: #FFF; text-transform: uppercase; font-size: 10px;font-family: sans-serif;font-weight: bold;text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.3)", "padding: 5px; border-radius: 0 4px 4px 0; background-color: #676767; color: #FFF; text-transform: uppercase; font-size: 10px;font-family: sans-serif", w)) : console.log("%cJS%cNo configuro publicKey", "padding: 5px; border-radius: 4px 0 0 4px; background-color: #38d9a9; color: #222b31; text-transform: uppercase; font-weight: bold; font-size: 10px;font-family: sans-serif", "padding: 5px; border-radius: 0 4px 4px 0; background-color: #ad1411; color: #FFF; text-transform: uppercase; font-size: 10px;font-family: sans-serif; font-weight: bold; text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.3)"), document.querySelector("#elements_frame_controller") == null && (this.iframe.setAttribute("src", e), this.iframe.setAttribute("class", "culqi-elements_controller"), this.iframe.setAttribute("id", "elements_frame_controller"), this.iframe.setAttribute("name", "elements_frame_controller"), this.iframe.setAttribute("allowtransparency", "true"), this.iframe.setAttribute("frameborder", "0"), this.iframe.style.height = "0px", this.iframe.style.width = "0px", document.body.appendChild(this.iframe)), window.addEventListener("message", function(C) {
                    var q = C.data;
                    if (d = null, p = null, q.type === "clq-element_autofocus") {
                        var o = "";
                        switch (q.element) {
                            case "expiry":
                                o = "Expiry";
                                break;
                            case "cvv":
                                o = "Cvc"
                        }
                        document.querySelector(".culqi-element_iframe[name = culqi-element_card" + o).contentWindow.postMessage({
                            type: "clq_focusElement"
                        }, x)
                    }
                    q.type == "clq-element_event" && (document.querySelectorAll(".culqi-element_iframe"), document.querySelector('.culqi-element_iframe[name="culqi-element_cardCvc"]').contentWindow.postMessage({
                        data: q.data,
                        type: "clq_setCVVMask"
                    }, x)), q.object == "token" ? (d = q, culqi()) : q.object == "error" && (p = q, culqi())
                }, !1)
            }
            var m, y, S;
            return m = n, (y = [{
                key: "create",
                value: function(w, C) {
                    return C === void 0 && (C = 0), new s.default(w, C)
                }
            }, {
                key: "sendData",
                value: function(w) {
                    var C, q = document.querySelector("#elements_frame_controller"),
                        o = document.querySelectorAll(".culqi-element_iframe");
                    q.contentWindow.postMessage({
                        type: "clq_restartElementsData"
                    }, e);
                    for (var v = 0; v < o.length; v++) o[v].contentWindow.postMessage({
                        type: "clq_getElementsData"
                    }, x), C = b(w) == "object" ? {
                        type: "clq_getElementsData",
                        metadata: w
                    } : {
                        type: "clq_getElementsData"
                    }, q.contentWindow.postMessage(C, e)
                }
            }, {
                key: "publicKey",
                get: function() {
                    return g
                },
                set: function(w) {
                    g = w
                }
            }, {
                key: "token",
                get: function() {
                    return d
                }
            }, {
                key: "error",
                get: function() {
                    return p
                }
            }]) && f(m.prototype, y), S && f(m, S), n
        }();
    c.default = E, I.exports = c.default
}, function(I, c, u) {
    "use strict";

    function l(f, d) {
        for (var p = 0; p < d.length; p++) {
            var g = d[p];
            g.enumerable = g.enumerable || !1, g.configurable = !0, "value" in g && (g.writable = !0), Object.defineProperty(f, g.key, g)
        }
    }
    Object.defineProperty(c, "__esModule", {
        value: !0
    }), c.default = void 0;
    var s = "https://checkout.culqi.com/v4/#/elements",
        b = function() {
            function f(x, e) {
                (function(E, n) {
                    if (!(E instanceof n)) throw new TypeError("Cannot call a class as a function")
                })(this, f), this.type = x, this.options = e, this.iframe = document.createElement("IFRAME"), this.iframe.setAttribute("src", s), this.iframe.setAttribute("class", "culqi-element_iframe"), this.iframe.setAttribute("name", "culqi-element_" + x), this.iframe.setAttribute("allowtransparency", "true"), this.iframe.setAttribute("frameborder", "0"), this.iframe.style.height = "inherit", this.iframe.style.width = "100%"
            }
            var d, p, g;
            return d = f, (p = [{
                key: "mount",
                value: function(x) {
                    var e = this;
                    document.querySelector(x).appendChild(e.iframe);
                    var E = document.querySelector(x + " iframe");
                    E.onload = function() {
                        E.contentWindow.postMessage({
                            data: e.options,
                            clqElementType: e.type,
                            type: "clq_setElementData"
                        }, s)
                    }
                }
            }, {
                key: "on",
                value: function(x, e) {
                    var E = this;
                    window.addEventListener("message", function(n) {
                        var m = E.type.toLowerCase();
                        n.data.type == "clq-element_status" && m == n.data.data.element.replace("-", "") && (x == "all" ? e && e({
                            event: n.data.event,
                            data: n.data.data
                        }) : n.data.event == x && e && e({
                            data: n.data.data
                        }))
                    }, !1)
                }
            }]) && l(d.prototype, p), g && l(d, g), f
        }();
    c.default = b, I.exports = c.default
}]);

var Culqi = new culqijs.Checkout;