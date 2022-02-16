<template>
<div id="diary" class="main-box">
    <div class="card text-center">
        <div class="card-header">
            Thermal Power Output
        </div>
        <div class="tabs">
            <Button
            v-for="tab in tabs"
            :key="tab.currentTab"
            :msg="tab.msg"
            class="btn btn-primary"
            @click="currentTab=tab.currentTab"
            />
            <component :is="currentTab"></component>
        </div>
        
    </div>
</div>
</template>

<script>
import WeeklyData from "../components/Diary/WeeklyData.vue"
import ViewFCData from "../components/Diary/ViewFCData.vue"
import Parent from "../components/Diary/ParentForms.vue"
import Child from "../components/Diary/ChildForms.vue"
import Table from "../components/Diary/Table.vue"
import Button from "../components/Diary/Button.vue"

export default {
    name: "Container",
    components: {
        WeeklyData,
        ViewFCData,
        Parent,
        Child,
        Table,
        Button,
    },
    data(){
        return {
            currentTab: "WeeklyData",
            tabs: [
                {msg:"Edit", currentTab: "WeeklyData"},
                {msg:"View", currentTab: "ViewFCData"},
            ]
        }
    }, 
    watch: {
        currentTab(){
            console.log(this.currentTab)
        }
    }
}
</script>
<style>
    #diary .row {
        position: relative;
    }
    #diary .col .fa-times {
        position: absolute;
        top:0;
        right:15px;
        color:red;
    }
    #diary .col .fa-link {
        position: absolute;
        top:0;
        right:40px;
        /* color:#0d6efd; */
    }
    .active {
        color:#0d6efd;
    }
    .inactive {
        color:grey;
    }
    .btn {
        width:25%;
        
    }
    .tabs > .btn-primary {
        background-color: rgba(0,0,0,.03);
        color:black;
    }
    .tabs > .btn-primary:hover {
        background-color: #d6d5d5;
        color:black;
    }
    .tabs > .btn-primary:focus {
        background-color: #d6d5d5;
        color:black;
    }

    #diary .col {
        width:33%;
    }
    #diary .table {
        width:100%;
        text-align: center;
    }
    .tabs {
        border: 1px solid #eee;
        border-radius: 2px;
        /* padding: 20px 30px; */
        margin-bottom: 5px;
        user-select: none;
        overflow-x: auto;
}
    .tabs > .btn {
        width: 50%;
        border-radius:0;
        border: 1.5px solid #eee;
    }
</style>