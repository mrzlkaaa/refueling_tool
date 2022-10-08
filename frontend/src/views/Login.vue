<template>
    <form method="post">
        <div class="container">
            <div class="forms-container">
                <h1>Welcome Back</h1> <br>  
                <div class="form-floating mb-3">
                    <i class="fa-solid fa-user fa-2xl"></i>    
                    <Input
                    id="floatingInput"
                    placeholder="Enter your password"
                    v-model="credentials.Username"
                    />
                    <Label
                    for="floatingInput"
                    text="Login"
                    />
                </div>
                <div class="form-floating mb-3">
                    <i class="fa-solid fa-key fa-2xl"></i>
                    <Input
                    type="password"
                    placeholder="Enter your password"
                    id="floatingInput"
                    v-model="credentials.Password"
                    />
                    <Label
                    for="floatingInput"
                    text="Password"
                    />
                </div>
                <Button
                cls="btn-primary"
                text="Sign in"
                @click="signIn"
                />
                <router-link :to='{name: "Register"}'>
                    <Button
                    cls="btn-link"
                    text="Register"
                    />
                </router-link>
                <!-- <router-view></router-view> -->
            </div>
        </div>
    </form>
</template>
<script>
import { mapActions } from 'vuex'
import Input from "../components/Input.vue"
import Label from "../components/Label.vue"
import Button from "../components/Button.vue"
export default {
    name: "Login",
    components:{
        Input,
        Label,
        Button,
    },
    data(){
        return {
            credentials:{
                Username: null,
                Password: null,
                cookie: true,
            }
            
        }
    },
    created(){
        //* if autologining seccusseful redirect to previous page
        this["auth/autologgining"]()
            .then(() =>this.$router.push({name: "List"}))
            .catch(err => console.error(err))
    },
    methods:{
        //todo add mapstate
        //! rename to nested modules
        ...mapActions(
            [
                "auth/login",
                "auth/autologgining",
                "api/makeFetch"
            ]
        ),
        async signIn(){
            console.log(process.env.NODE_ENV)
            const req = {
                url: `${this.authDepHost}/login`,
                method: "POST",
                data: this.credentials,
                auth: null,
            }
            console.log(req)
            let results = await this['api/makeFetch'](req)
            if (results){
                await this["auth/login"]({...results, ...this.credentials})
                setTimeout(this.$router.push, 500, {name:"List"})
            }
        }
    },
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
        left:-35px;
    }
    .fa-key{
        position:absolute;
        top: 30px;
        left:-38px;
    }
</style>