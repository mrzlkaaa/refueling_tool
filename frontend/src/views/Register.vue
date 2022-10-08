<template>
    <form method="post">
        <div class="container">
            <h1>Welcome</h1> <br>
            <div class="forms-container">
                <div class="form-floating mb-3">
                    <i class="fa-solid fa-user fa-2xl"></i>
                    <Input
                    type="text"
                    placeholder="Enter your name"
                    id="floatingInput1"
                    v-model="credentials.Name"
                    />
                    <Label
                    for="floatingInput1"
                    text="Name"
                    />
                </div>
                <div class="form-floating mb-3">
                    <i class="fa-solid fa-user fa-2xl"></i>
                    <Input
                    type="text"
                    placeholder="Enter your surname"
                    id="floatingInput2"
                    v-model="credentials.Surname"
                    />
                    <Label
                    for="floatingInput2"
                    text="Surname"
                    />
                </div>
                <div class="form-floating mb-3">
                    <i class="fa-solid fa-user-gear fa-2xl"></i>
                    <Input
                    type="text"
                    placeholder="Enter your username"
                    id="floatingInput3"
                    v-model="credentials.Username"
                    />
                    <Label
                    for="floatingInput3"
                    text="Login"
                    />
                </div>
                <div class="form-floating mb-3">
                    <i class="fa-solid fa-envelope fa-2xl"></i>
                    <Input
                    type="email"
                    name="email"
                    id="floatingInputEmail4"
                    placeholder="Enter your email"
                    v-model="credentials.Email"
                    />
                    <Label
                    for="floatingInputEmail4"
                    text="Email"
                    />
                </div>
                <div class="form-floating mb-3">
                    <i class="fa-solid fa-lock fa-2xl"></i>
                    <Input
                    type="password"
                    placeholder="Enter your password"
                    id="floatingInput5"
                    v-model="credentials.Password"
                    />
                    <Label
                    for="floatingInput5"
                    text="Password"
                    />
                </div>
                <div class="form-floating mb-3">
                    <i class="fa-solid fa-key fa-2xl"></i>
                    <Input
                    type="password"
                    placeholder="Enter your password"
                    id="floatingInput6"
                    v-model="credentials.Password2"
                    />
                    <Label
                    for="floatingInput6"
                    text="Repeat Password"
                    />
                </div>
                <Button
                :dis=disabled
                cls="btn-primary"
                text="Sign up"
                @click="signUp"
                />
                <router-link :to='{name: "Login"}'>
                    <Button
                    cls="btn-link"
                    text="Login"
                    />  
                </router-link>
            </div>
        </div>
    </form>
</template>
<script>
import {mapActions, mapGetters} from "vuex"
import Input from "../components/Input.vue"
import Label from "../components/Label.vue"
import Button from "../components/Button.vue"
export default {
    name: "Register",
    components:{
        Input,
        Label,
        Button,
    },
    data(){
        return {
            disabled:true,
            credentials:{
                Name:"",
                Surname: "",
                Username: '',
                Email:'',
                Password: '',
                Password2: '',
            }
        }
    },
    methods:{
        ...mapGetters('auth', [
            "isAccess",
        ]),
        ...mapActions([
            "api/makeFetch",
            "alert/alertSuccess",
        ]),
        async signUp(){ //! must be fixed according to new style
            const req = {
                url: `${this.authDepHost}/register`,
                method: "POST",
                data: this.credentials,
                auth: null, //todo access via getter
            }
            let results = await this['api/makeFetch'](req)
            if (results){
                this['alert/alertSuccess']({msg:results})
                setTimeout(this.$router.push, 1000, {name:"Login"})
            }
        }
    },
    watch:{
        credentials:{
            deep:true,
            handler(){
                let status = false
                Object.values(this.credentials).forEach((e) =>{
                    if (e.length > 0) {
                        if (this.credentials.Password == this.credentials.Password2 && 
                                this.credentials.Password.length > 0 && this.credentials.Password2.length > 0){
                            console.log("ok in pass")
                            status = false
                        }
                        else {
                            status = true
                        }
                    }
                    this.disabled = status
                })
            }
        }
    }
}
</script>

<style scoped>
    .forms-container {
        
        width:30%; 
        margin:auto;
    }
    .form-floating mb-3{
        position: relative;
        
    }
    .fa-user {
        position:absolute;
        top: 30px;
        left:-46px;
    }
    .fa-user-gear {
        position:absolute;
        top: 30px;
        left:-46px;
    }
    .fa-envelope{
        position:absolute;
        top: 30px;
        left:-46px;
    }
    .fa-lock{
        position:absolute;
        top: 30px;
        left:-43px;
    }
    .fa-key{
        position:absolute;
        top: 30px;
        left:-46px;
    }
    
</style>