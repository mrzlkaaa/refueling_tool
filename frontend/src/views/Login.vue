<template>
    <form method="post">
        <div class="container">
            <AlertBox
            :info="getAlert()"
            />
            <h1>Welcome Back</h1> <br>
            <div class="forms-container">
                
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
                <!-- <div class="form-check" style='width:40%'>
                    <Input
                    type="checkbox"
                    class="form-check-input"
                    id="flexCheckDefault"
                    />
                    <Label
                    class="form-check-label"
                    for="flexCheckDefault"
                    text="Stay logged"
                    />
                </div> <br> -->
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
import { mapActions, mapGetters } from 'vuex'
import Input from "../components/Input.vue"
import Label from "../components/Label.vue"
import Button from "../components/Button.vue"
import AlertBox from "../components/AlertBox.vue"
export default {
    name: "Login",
    components:{
        Input,
        Label,
        Button,
        AlertBox,
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
    methods:{
        //todo add mapstate
        ...mapGetters([
            "getAlert"
        ]),
        ...mapActions(
            [
                "alertError",
                "login",
                "makeFetch",
            ]
        ),
        async signIn(){
            console.log(this.data)
            const req = {
                url: `${this.authDepHost}/login`,
                method: "POST",
                data: this.credentials,
                auth: null,
            }
            let results
            try{
                const res = await this.makeFetch(req)
                if (res.ok){
                    results = await res.json()
                    console.log(results)
                    this.login({...results, ...this.credentials})
                    this.$router.push({name:"List"})
                }
                else {
                    results = await res.json()
                    let data = {
                        msg:results,
                    }
                    this.alertError(data)
                }
            }
            catch (error) {
                console.log(error)
            }
        }
    },
}
</script>

<style>
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