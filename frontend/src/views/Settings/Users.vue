<template>
    <div class="c">
        <AlertBox v-if="alert.display"
        :type="alert.type"
        :text="alert.msg"
        :time="alert.time"
        :code="alert.code"
        />
        <div class="row">
            <div id="users-header" class="col" v-for="h,i in header" :key="i">
                <b>{{h}}</b>
            </div>
        </div>
        <div id="users" class="row" v-for="c,i in content" :key="i">
            <div class="col" v-for="cc,ii in c" :key=ii>
                <Checkbox 
                v-if=isBoolean(cc)
                :status="cc"
                :text="cc"
                @toggle-checkbox="toggleCheckbox(i, ii)"
                />
                <div v-else>{{cc}}</div>
            </div>
            <i @click="onDelete(c.ID)" class="fas fa-times"></i>
        </div>
        <br>
        <div class="row">
            <div class="col"></div>
            <div class="col">
                <Button
                cls="btn-primary to-right"
                text="Save"
                width="10"
                :dis="disabled"
                @click="onSave"
                />
            </div>
        </div>
        
    </div>
    
</template>
<script>
import Checkbox from "../../components/Checkbox.vue"
import Button from "../../components/Button.vue"
import AlertBox from "../../components/AlertBox.vue"
export default {
    name: "Users",
    components: {
        Checkbox,
        Button,
        AlertBox,
    },
    data(){
        return {
            dat:{
                code : 200,
                msg: "",
            },
            header: ["ID",'Name', "Surname", "Email", "Username", "Moderator", "Admin"],
            content:[],
            origin: [],
            onChange: [],
            disabled:true,
        }
    },
    methods:{
        isBoolean:(value) => {
            if (typeof(value) == "boolean"){
                return true
            }
            return false
        },
        toggleCheckbox(i, ii){
            let nameCheck = this.onChange.some((e)=> e.Username == this.content[i].Username)
            if (!nameCheck) {
                this.content[i][ii] = !this.content[i][ii]
                this.onChange.push(this.content[i])

            }
            else {
                this.onChange = this.onChange.filter(e => e.Username != this.content[i].Username)
                this.content[i][ii] = !this.content[i][ii]
                this.onChange.push(this.content[i])
            }
            let matchedInd = []
            for (let i = 0; i < this.origin.length; i++) {
                let originJSON = JSON.stringify(this.origin[i])
                for (let j = 0; j < this.onChange.length; j++) {
                    let onChangeJSON = JSON.stringify(this.onChange[j])
                    if (originJSON === onChangeJSON){
                        matchedInd.push(j)
                    }
                }
            }
            if (matchedInd.length > 0) {
                matchedInd.map(i => this.onChange.splice(i, 1))
            }
        },
        onDelete(id){
            if (confirm(`Are you sure you want to delete ${id}?`)){ 
                const request = new Request(
                `${this.authDepHost}/users/${id}/delete`,
                    {
                        method: "POST",
                        headers: {
                                "Authorization": this.$store.state.accessToken,
                                'Accept': 'application/json',
                                "Content-Type": "application/json",
                                },
                        // body: JSON.stringify(id)
                    }
                )
                fetch(request)
                .then(response => {
                    this.dat.code=response.status
                    return response.json()
                })
                .then(data => {
                    this.dat.msg = data
                    switch (data){
                        case "token is expired":
                            this.$store.dispatch("refreshTokens", this.authDepHost)
                            break;
                        case "you are not eligible for this service":
                            this.$store.dispatch("alertWarning", this.dat)
                            //todo add smth like "contact admin" and form appears
                            break;
                        default:
                            if (this.dat.code==200){
                                this.$store.dispatch("alertSuccess", this.dat.msg)
                                this.content = this.content.filter(e => e.ID != id)
                            }
                            else {
                                this.$store.dispatch("alertError", this.dat)
                            }
                            
                            // this.$store.dispatch("alertError", data)
                    }
                    // setTimeout(this.$router.push, 1000, {name:"Users"})
                })
                .catch(error => console.log(error.message))
            }
        },
        onSave(){

        }
    },
    watch:{
        onChange:{
            deep:true,
            handler(){
                if (this.onChange.length > 0){
                    //todo add condition to check if the data equals to origin
                    this.disabled = false
                }
                else{
                    this.disabled = true
                }
            }
        }
    },
    created(){
        const request = new Request(
            `${this.authDepHost}/getusers`,
            {
                method: "GET",
                headers: {
                        "Authorization": this.$store.state.accessToken,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        }
            }
        )
        fetch(request)
            .then(response => {
                this.dat.code=response.status                
                return response.json()
            })
            .catch(error => console.log(error))
            .then(data => {
                console.log(data)
                this.dat.msg = data
                switch (data){
                    case "token is expired":
                        this.$store.dispatch("refreshTokens", this.authDepHost)
                        break;
                    case "you are not eligible for this service":
                        this.$store.dispatch("alertWarning", this.dat)
                        //todo add smth like "contact admin" and form appears
                        break;
                    default:
                        if (this.dat.code==200){
                            this.content = data
                            this.origin = JSON.parse(JSON.stringify(data))
                        }
                        // else {
                        //     // setTimeout(this.$router.push, 4000, {name:"Login"})
                        // }
                }
            })
            .catch(error => console.log(`catched ${error}`))
    },
    computed:{
        alert(){
            return this.$store.state.alert
        }
    }
}
</script>
<style>
    #users-header{
        padding-bottom: 7px;
    }
    #users {
        position: relative;
        padding-top: 7px;
        padding-bottom:7px;
        text-align: center;
    }
    #users:hover {
        background: #eee;
    }
    .to-right{
        float: right;
        /* margin-left:auto;
        margin-right:0; */
    }
    #users .fa-times {
        position: absolute;
        color: red;
        width:10px;
        top:11px;
        right:0;
    }
</style>
