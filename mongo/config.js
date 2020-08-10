rs.initiate( {
   _id : "rs0",
   members: [
      { _id: 0, host: "mongo_1:27017" },
      { _id: 1, host: "mongo_2:27017" },
      { _id: 2, host: "mongo_3:27017" }

   ]
})
