<template>
    <table class="table">
        <thead>
            <TableRowHeader
            :datas="header"
            />
        </thead>
        <tbody>
            <TableRowBody
            :datas="data"
            />
        </tbody>
    </table>
</template>
<script>
import TableRowHeader from "./TableRowHeader.vue"
import TableRowBody from "./TableRowBody.vue"
export default {
    name: "Table",
    components:{
        TableRowHeader,
        TableRowBody,
    },
    props: ["data"],
    data(){
        return{
            header: ['AR', "KO1", "KO2", "KO3", "Temperature"]
        }
    }
}
</script>