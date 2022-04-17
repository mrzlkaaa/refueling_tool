<template>
    <form method="post">
        <div class="container">
            <h1>Welcome</h1> <br>
            <div class="forms-container">
                <div class="form-floating mb-3">
                    <i class="fa-solid fa-user fa-2xl"></i>
                    <Input
                    type="text"
                    placeholder="Enter your username"
                    id="floatingInput1"
                    v-model="credentials.Username"
                    />
                    <Label
                    for="floatingInput1"
                    text="Login"
                    />
                </div>
                <div class="form-floating mb-3">
                    <i class="fa-solid fa-envelope fa-2xl"></i>
                    <Input
                    type="email"
                    name="email"
                    id="floatingInputEmail2"
                    placeholder="Enter your email"
                    v-model="credentials.Email"
                    />
                    <Label
                    for="floatingInputEmail2"
                    text="Email"
                    />
                </div>
                <div class="form-floating mb-3">
                    <i class="fa-solid fa-lock fa-2xl"></i>
                    <Input
                    type="password"
                    placeholder="Enter your password"
                    id="floatingInput3"
                    v-model="credentials.Password"
                    />
                    <Label
                    for="floatingInput3"
                    text="Password"
                    />
                </div>
                <div class="form-floating mb-3">
                    <i class="fa-solid fa-key fa-2xl"></i>
                    <Input
                    type="password"
                    placeholder="Enter your password"
                    id="floatingInput4"
                    v-model="credentials.Password2"
                    />
                    <Label
                    for="floatingInput4"
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
            dat:{
                code:200,
                msg:'',
            },
            disabled:true,
            credentials:{
                Username: '',
                Email:'',
                Password: '',
                Password2: '',
            }
        }
    },
    methods:{
        signUp(){
            const request = new Request(
            `${this.authDepHost}/register`,
            {
                method: "POST",
                headers: { 
                        // 'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        },
                body: JSON.stringify(this.credentials)
            });
            fetch(request)
                .then(response => {
                    this.dat.code=response.status
                    return response.json()
                })
                .then(data => {
                    console.log(data)
                    // this.$store.dispatch()
                    // this.$store.dispatch("login", joined)
                    this.$router.push({name:"Login"})
                })
                .then(err => console.log(err)) //todo force to appear info-message box

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
        left:-37px;
    }
    .fa-envelope{
        position:absolute;
        top: 30px;
        left:-40px;
    }
    .fa-lock{
        position:absolute;
        top: 30px;
        left:-37px;
    }
    .fa-key{
        position:absolute;
        top: 30px;
        left:-40px;
    }
    
</style>