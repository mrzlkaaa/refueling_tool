<template>
    <div class="c">
        <div>
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
    </div>
    
</template>
<script>
import {mapGetters, mapActions} from "vuex"
import Modal from "../../components/Modal.vue"
import Checkbox from "../../components/Checkbox.vue"
import Button from "../../components/Button.vue"
import AlertBox from "../../components/AlertBox.vue"
export default {
    name: "Users",
    components: {
        Modal,
        Checkbox,
        Button,
        AlertBox,
    },
    data(){
        return {
            showModal:true,
            display: true,
            header: ["ID",'Name', "Surname", "Email", "Username", "Moderator", "Admin"],
            content:[],
            origin: [],
            onChange: [],
            disabled:true,
        }
    },
    methods:{
        ...mapGetters([
            
            
            "isAccess"
        ]),
        ...mapActions([
            "makeFetch",
            "alertSuccess",
        ]),
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
        async onDelete(id){
            if (confirm(`Are you sure you want to delete user ${id}?`)){
                const req = {
                    url: `${this.authDepHost}/users/${id}/delete`,
                    method: "POST",
                    data: null,
                    auth: this.isAccess(),
                }
                let results = await this.makeFetch(req)
                if (results){
                    this.alertSuccess({msg:results})
                    this.content = this.content.filter(e => e.ID != id)
                    this.origin = JSON.parse(JSON.stringify(this.content))
                    this.onChange = []
                }
                
            }
        },
        async onSave(){
            const req = {
                url: `${this.authDepHost}/users/update`, //todo on change
                method: "POST",
                data: this.onChange,
                auth: this.isAccess(),
            }
            console.log(req)
            let results = await this.makeFetch(req)
            if (results){
                this.alertSuccess({msg:results})
                this.origin = JSON.parse(JSON.stringify(this.content))
                this.onChange = []
            }
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
    async created(){
        const req = {
            url: `${this.authDepHost}/getusers`,
            method: "GET",
            data: null,
            auth: this.isAccess(),
        }
        let results = await this.makeFetch(req)
        if (results){
            this.content = results
            this.origin = JSON.parse(JSON.stringify(this.content))
        }
    },
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
