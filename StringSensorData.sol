pragma solidity ^0.5.16;

// contract name
contract StringSensorData{
         //Initilizes varibles used later within the code
         address owner;
         string sensorData;

        constructor() public
        {
            //Sets sensor data to an empty value
            sensorData = '';
           
            owner = msg.sender;
        }

        function setSensorData(string memory _sensorData) public
        {
          require(msg.sender == owner);
          sensorData = _sensorData;
        }

        function getSensorData() public view returns(string memory){
          return sensorData;
        }

}
