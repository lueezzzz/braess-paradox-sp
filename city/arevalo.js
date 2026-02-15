intersections = [
  {
    id: "villa - 1",
    name: "Osmena St - Jocson St",
    latitude: 10.688897,
    longitude: 122.5164,
    connections: ["villa - 2", "villa - 4"],
  },
  {
    id: "villa - 2",
    name: "Iloilo Circumrferential Rd 1 - Jocson St",
    latitude: 10.688957,
    longitude: 122.521095,
    connections: ["villa - 1", "villa - 3"],
    // [3,4, Iloilo Circumferential Rd 1]
  },
  {
    id: "villa -3",
    name: "Jocson St - Quezon St",
    latitude: 10.688729,
    longitude: 122.526827,
    connections: ["villa - 2", "villa - 4"],
    // [1,4, Avacena]
  },
  {
    id: "villa - 4",
    name: "Osmena St - Yulo Dr",
    latitude: 10.688957,
    longitude: 122.521095,
    connections: ["villa - 1", "villa - 3"],
  },
];

roads = [
  // {
  //     name: "Osmena St",
  //     A: "villa - 1",
  //     B: ,
  //     distance: ,
  //     lanes: 2,
  //     one_way: false,
  // },
  // {
  //     name: "Molo Blvd",
  //     A: ,
  //     B: ,
  //     distance: ,
  //     lanes: 2,
  //     one_way: false,
  // },
  {
    name: "Yulo Dr",
    A: "villa - 1",
    B: "villa - 4",
    distance: 200,
    lanes: 2,
    one_way: false,
  },
  {
    name: "Quezon St",
    A: "villa - 3",
    B: "villa - 4",
    distance: 1100,
    lanes: 2,
    one_way: false,
  },
  // {
  //     name: "Iloilo Circumferential Rd 1",
  //     A: "villa - 2",
  //     B: ,
  //     distance: ,
  //     lanes: 2,
  //     one_way: false,
  // },
  {
    name: "Jocson St",
    A: "villa - 1",
    B: "villa - 3",
    distance: 1100,
    lanes: 2,
    one_way: false,
  },
];
