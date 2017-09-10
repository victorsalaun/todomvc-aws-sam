import apigClientFactory from 'aws-api-gateway-client'

export default class Client {

    constructor() {
        this.config = {
            invokeUrl: 'https://tso7cmvr08.execute-api.eu-central-1.amazonaws.com/current',
            service: 'execute-api',
            region: 'eu-central-1'
        };
        this.apigClient = apigClientFactory.newClient(this.config)
    }

    callApi(params, pathTemplate, method, additionalParams, body, success, error) {
        this.apigClient.invokeApi(params, pathTemplate, method, additionalParams, body)
            .then(function (result) {
                success(result.data)
            }).catch(function (result) {
            error(result)
        })
    }

    init() {
    }

    // very primitive change listener
    onChange() {
    }

}

Client.install = function (Vue) {
    Object.defineProperty(Vue.prototype, '$client', {
        get() {
            return this.$root._client
        }
    });

    Vue.mixin({
        beforeCreate() {
            if (this.$options.client) {
                this._client = this.$options.client;
                this._client.init(this)
            }
        }
    })
};
