<template>
    <tr>
        <th v-for="data in header" :key="data">
            {{data}}
        </th>
    </tr>
</template>
<script>
export default {
    name: "TableRowHeader",
    inject:["header"],
}
</script>