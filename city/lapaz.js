intersections = [
  {
    id: "lapaz - 1",
    name: "Luna St - Huervana St",
    latitude: 10.707804,
    longitude: 122.567107,
    connections: ["lapaz - 2", "lapaz - 3"], // [Capitol]
  },
  {
    id: "lapaz- 2",
    name: "Rizal St - Luna St",
    latitude: 10.708378,
    longitude: 122.567858,
    connections: ["lapaz - 1", "lapaz - 3", "lapaz - 4"],
  },
  {
    id: "lapaz - 3",
    name: "Luna St - Luna St",
    latitude: 10.709190,
    longitude: 122.568400,
    connections: ["lapaz - 1", "lapaz - 2"], // [Nelly]
  },
  {
    id: "lapaz - 4",
    name: "Huervana St - Jereos St",
    latitude: 10.710460,
    longitude: 122.570379,
    connections: ["lapaz - 2", "lapaz - 5", "lapaz - 7"],
  },
  {
    id: "lapaz - 5",
    name: "Jereos St - Huervana Ext",
    latitude: 10.711606,
    longitude: 122.571909,
    connections: ["lapaz - 4", "lapaz - 6", "lapaz - 8"],
  },
  {
    id: "lapaz - 6",
    name: "Huervana Ext - Burgos St",
    latitude: 10.713029,
    longitude: 122.570879,
    connections: ["lapaz - 5", " lapaz - 7"], // [Jereos to Jaro]
  },  
  {
    id: "lapaz - 7",
    name: "Burgos St - Huervana St",
    latitude: 10.711777,
    longitude: 122.569511,
    connections: ["lapaz - 4", " lapaz - 6"], // [Burgos to Jaro]
  },
  {
    id: "lapaz - 8",
    name: "Lopez Jaena St - Baldoza St",
    latitude: 10.714284,
    longitude: 122.572201,
    connections: ["lapaz - 5", "lapaz - 9"],
  },
  {
    id: "lapaz - 9",
    name: "Baldoza St - Monfort Blvd",
    latitude: 10.713908,
    longitude: 122.581449,
    connections: ["lapaz - 8"], //[8, Coastal Rd, Monfort Blvd]
  },
  {
    id: "lapaz - 10",
    name: "Luna St - Taytay Forbes",
    latitude: 10.706364,
    longitude: 122.567494,
    connections: ["lapaz - 1"], //[Bonifacio Dr, Lapuz]
  },
];

roads = [
  {
      name: "Luna St",
      A: "lapaz - 10",
      B: "", //[Luna St, Jaro]
      distance: ,
      lanes: 2,
      one_way: false,
  },
  {
      name: "Rizal St - Luna St",
      A: "lapaz - 2",
      B: "lapaz - 3", 
      distance: ,
      lanes: 1,
      one_way: true,
  },
  {
      name: "Huervana St - Rizal St",
      A: "lapaz - 1",
      B: "lapaz - 2",
      distance: ,
      lanes: 1,
      one_way: true,
  },
  {
      name: "Huervana St - Burgos St",
      A: "lapaz - 2",
      B: "lapaz - 4",
      distance: ,
      lanes: 2,
      one_way: false,
  },
  {
      name: "Huervana St - Jereos St",
      A: "lapaz - 4",
      B: "lapaz - 5",
      distance: ,
      lanes: 1,
      one_way: true,
  },
  {
      name: "Jereos St - Huervana Ext",
      A: "lapaz - 5",
      B: "lapaz - 6",
      distance: ,
      lanes: 1,
      one_way: true,
  },
  {
      name: "Huervana Ext",
      A: "lapaz - 6",
      B: "lapaz - 7",
      distance: ,
      lanes: 1,
      one_way: true,
  },
  {
      name: "Burgos St - Huervana St",
      A: "lapaz - 7",
      B: "lapaz - 4",
      distance: ,
      lanes: 1,
      one_way: true,
  },
  {
      name: "Lopez Jaena St",
      A: "lapaz - 5",
      B: "lapaz - 8",
      distance: ,
      lanes: 2,
      one_way: false,
  },
  {
      name: "Baldoza St",
      A: "lapaz - 8",
      B: "lapaz - 9",
      distance: ,
      lanes: 2,
      one_way: false,
  },
  {
      name: "Coastal Rd",
      A: "lapaz - 9",
      B: "", //[Lapuz]
      distance: ,
      lanes: 2,
      one_way: false,
  },
  {
      name: "Monfort Blvd",
      A: "lapaz - 9",
      B: "", //Monfort [Jaro]
      distance: ,
      lanes: 2,
      one_way: false,
  },
  {
      name: "Burgos St",
      A: "lapaz - 7",
      B: "", //[Burgos, Jaro]
      distance: ,
      lanes: 2,
      one_way: false,
  },
  {
      name: "Jereos St",
      A: "lapaz - 5",
      B: "lapaz - 6",
      distance: ,
      lanes: 2,
      one_way: false,
  },
];