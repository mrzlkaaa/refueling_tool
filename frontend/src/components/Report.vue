<template>
    <transition name="modal">
        <form ref="mailform" >
            <div class="modal-container">
                    
                    <i class="fas fa-times fa-lg" @click="hideForm"></i>
                    <h4>Leave your feedback here!</h4> <br>
                    
                    <div class="form-floating mb-3">
                        <Input
                        type="text"
                        id="floatingInput1"
                        v-model="form.from_name"
                        name="from_name"
                        />
                        <Label
                        for="floatingInput1"
                        text="From"
                        />
                    </div>
                    <div class="form-floating mb-3">
                        <TextArea
                        placeholder="Enter your username"
                        name="message"
                        id="floatingInput3"
                        v-model="form.message"
                        />
                        <Label
                        for="floatingInput3"
                        text="Message"
                        />
                    </div>
                    <Button
                    v-if="!hideBtn"
                    type="submit"
                    :dis=disabled
                    cls="btn-primary"
                    text="Submit"
                    @click.prevent="sendEmail"
                    />
                    <div v-else class="lds-ring"><div></div><div></div><div></div><div></div></div>
            </div>
        </form>
    </transition>
</template>
<script>
import emailjs from '@emailjs/browser';
import {mapActions, mapGetters} from "vuex"
import Input from "./Input.vue"
import TextArea from "./TextArea.vue"
import Label from "./Label.vue"
import Button from "./Button.vue"
export default {
    name: "Report",
    components:{
        Input,
        Label,
        Button,
        TextArea
    },
    data(){
        return {
            form: {
                "from_name": this.isAuthenticated(),
                "message": "",
            },
            hideBtn:false
        }
    },
    created(){
        console.log("Created")
        this.hideBtn = false
    },
    methods:{
        ...mapGetters([
            "isAccess",
            "isAuthenticated",
            "isDisplayed"
        ]),
        ...mapActions([
            "hideForm"
        ]),
        async sendEmail() {
            this.hideBtn = true;
            emailjs.sendForm('service_oc01nsm', 'template_mlft898', this.$refs.mailform, 'sdZU9_0SPhGqeKHgm')
                .then((result) => {
                    console.log('SUCCESS!', result.text); //!call of vuex action
                    this.hideForm()

                }, (error) => {
                    console.log('FAILED...', error.text); //!call of vuex action
                    this.hideBtn = false;
                });
            }
        }
}
</script>
<style scoped>
    /* .modal-mask {
        position: fixed;
        z-index: 9998;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: table;
        transition: opacity 0.3s ease;
    } */

    /* .modal-wrapper {
        display: table-cell;
        vertical-align: middle;
    } */

    .modal-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 400px;
        margin: 0px auto;
        padding: 20px 20px;
        background-color: #fff;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
        transition: all 0.3s ease;
        font-family: Helvetica, Arial, sans-serif;
    }

    @-webkit-keyframes modal-container {
    100% { left: 0; }
    }

    @keyframes modal-container {
        100% { left: 0; }
    }

    .modal-header h3 {
        margin-top: 0;
        color: #42b983;
    }

    .modal-body {
        margin: 20px 0;
    }

    /*
    * The following styles are auto-applied to elements with
    * transition="modal" when their visibility is toggled
    * by Vue.js.
    *
    * You can easily play with the modal transition by editing
    * these styles.
    */

    /* .modal-enter {
        opacity: 0;
    }

    .modal-leave-active {
        opacity: 0;
    }

    .modal-enter .modal-container,
    .modal-leave-active .modal-container {
        -webkit-transform: scale(1.1);
        transform: scale(1.1);
    } */


    .fa-times {
        position: absolute;
        right: 20px;
        top:33px;
    }
    .lds-ring {
        display: inline-block;
        position: relative;
        /* margin:auto; */
        width: 35px;
        height: 35px;
    }
    .lds-ring div {
        box-sizing: border-box;
        display: block;
        position: absolute;
        width: 35px;
        height: 35px;
        border: 2px solid #fff;
        border-radius: 50%;
        animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
        border-color: black transparent transparent transparent;
    }
    .lds-ring div:nth-child(1) {
        animation-delay: -0.45s;
    }
    .lds-ring div:nth-child(2) {
        animation-delay: -0.3s;
    }
    .lds-ring div:nth-child(3) {
        animation-delay: -0.15s;
    }
    @keyframes lds-ring {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
    }
</style>