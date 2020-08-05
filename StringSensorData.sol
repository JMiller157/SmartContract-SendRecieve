pragma solidity ^0.5.16;

contract StringSensorData{
         address owner;
         string sensorData;

        constructor() public
        {
            sensorData = '0';
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
