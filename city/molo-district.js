intersections = [
  // {
  //   id: "Molo - 1",
  //   name: "Locsin St - New Carpenter's Bridge",
  //   latitude: 10.699186,
  //   longitude: 122.542524,
  //   connections: ["Molo - 2"], // + connect outside sa molo
  // },
  // {
  //   id: "Molo - 2",
  //   name: "Locsin St - San Jose St.",
  //   latitude: 10.698215,
  //   longitude: 122.542886,
  //   connections: ["Molo - 1", "Molo - 3"],
  // },
  {
    id: "Molo - 3",
    name: "Locsin St - San Marcos St.",
    latitude: 10.697347,
    longitude: 122.543396,
    connections: ["Molo - 4", "villa - 3"],
  },

  {
    id: "Molo - 4",
    name: "Locsin St. - M.H Del Pilar St. 2",
    latitude: 10.695993,
    longitude: 122.544452,
    connections: ["Molo - 3", "Molo - 5"],
  },
  {
    id: "Molo - 5",
    name: "Locsin St. - Timawa St.",
    latitude: 10.694449,
    longitude: 122.545638,
    connections: ["Molo - 4", "Molo - 6", "Proper - 2"],
  },
  {
    id: "Molo - 6",
    name: "Locsin St. - Baluarte - Calumpag - Villa - Oton Blvd",
    latitude: 10.692042,
    longitude: 122.549359,
    connections: ["Molo - 5", "Proper - 4"],
  },
  {
    id: "Molo - 7",
    name: "San Marcos St. - MH del Pilar St. 1",
    latitude: 10.699243,
    longitude: 122.549363,
    connections: ["Molo - 3", "Proper - 1"],
  },
  {
    id: "Molo - 8",
    name: "M.H Del Pilar St. 2",
    latitude: 10.698916,
    longitude: 122.549449,
    connections: ["Molo - 3", "Proper - 1"],
  },
];

roads = [
    // {
    //     name: "Locsin St. 1",
    //     A: "Molo - 1",
    //     B: "Molo - 2",
    //     distance: 120,
    //     lanes: 2,
    //     one_way: false,
    // },
    // {
    //     name: "Locsin St. 2",
    //     A: "Molo - 2",
    //     B: "Molo - 3",
    //     distance: 110,
    //     lanes: 2,
    //     one_way: false,
    // },
        {
        name: "Molo - 3 -> Villa - 3",
        A: "Molo - 3",
        B: "villa - 3",
        distance: 2100,
        lanes: 4,
        one_way: false,
    },
    {
        name: "Molo - 3 -> Molo - 4",
        A: "Molo - 3",
        B: "Molo - 4",
        distance: 190,
        lanes: 2,
        one_way: false,
    },
    {
        name: "Molo - 4 -> Molo - 5",
        A: "Molo - 4",
        B: "Molo - 5",
        distance: 220,
        lanes: 2,
        one_way: false
    },
    {
        name: "Molo - 5 -> Molo - 6",
        A: "Molo - 5",
        B: "Molo - 6",
        distance: 500,
        lanes: 4,
        one_way: false,
    },
    {
        name: "Molo - 7 -> Molo - 3",
        A: "Molo - 7",
        B: "Molo - 3",
        distance: 700,
        lanes: 4,
        one_way: true,
    },
        {
        name: "Molo - 8 -> Proper - 1",
        A: "Molo - 8",
        B: "Proper - 1",
        distance: 550,
        lanes: 4,
        one_way: true,
    }

];
