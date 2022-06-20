// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;


contract Election {

    struct Candidate {
        string name;
        uint voteCount;
        //uint candidateId;
    }

    struct Voter {
        string voterUsername;
        bool hasVoted;
    }
    
    struct Vote {
        address voterAddress;
        //uint candidateId;
        string candidateName;
    }


    address private owner; 
    string private electionName;

    mapping(address => Voter) private voters;
    mapping(uint => Vote) private votes;

    mapping(string => Candidate) private candidateMap;

    uint private candidateIDs = 0;
    uint private numOfCandidates = 0;
    string[] private candidateNames;


    enum VotingStates {AddCandidate,AddVoter,Voting,Finish}

    VotingStates private votingState;


    uint private numberOfVoters = 0;

    modifier adminOnly() {
        require(msg.sender == owner);
        _;
    }

    modifier isInThisState(VotingStates voteState){
        require(voteState == votingState);
        _;
    }

    modifier isLaterThanThisState(VotingStates voteState){
        require(voteState >= votingState);
        _;
    }

    constructor(string memory Name) {
        owner = msg.sender;
        votingState = VotingStates.AddCandidate;
        electionName = Name;
    }

    //ADD CANDIDATES STATE

    function addCandidate(string memory Name) public 
    adminOnly
    isInThisState(VotingStates.AddCandidate)
    {
        Candidate memory newCandidate;
        newCandidate.name = Name;
        newCandidate.voteCount = 0;
        //newCandidate.candidateId = candidateIDs;
        
        candidateNames.push(Name);
        candidateMap[Name] = newCandidate;
        candidateIDs +=1;
    }

    function getElectionName() public view returns(string memory) 
    {
        return electionName;
    }



    //ADD VOTER STATE
    function nextStateAddVoter() public
    adminOnly
    isInThisState(VotingStates.AddCandidate)
    {
        votingState = VotingStates.AddVoter;
    }



    function getNumOfCandidates() public 
    isLaterThanThisState(VotingStates.AddVoter)
    view returns(uint) 
    {
        return candidateNames.length;
    }

    function getCandidateNames() public 
    isLaterThanThisState(VotingStates.AddVoter)
    view returns (string[] memory)
    {  
        return candidateNames;
    }

    function AddVoter(string memory VoterUsername, address VoterAddress) public
    adminOnly
    isInThisState(VotingStates.AddVoter)
    {
        Voter memory newVoter;
        newVoter.voterUsername = VoterUsername;
        newVoter.hasVoted = false;
        voters[VoterAddress] = newVoter;
        numberOfVoters += 1;
    }



    //VOTE STATE
    function nextStateVoting() public
    adminOnly
    isInThisState(VotingStates.AddVoter)
    {
        votingState = VotingStates.Voting;
    }


    function VotingProgressing(string memory CandidateName) public
    isInThisState(VotingStates.Voting)
    returns (bool hasVoterVoted)
    {
        bool hasValidVoterAddress = false;

        if(bytes(voters[msg.sender].voterUsername).length > 0  &&  voters[msg.sender].hasVoted == false)
        {
            Vote memory newVote;
            newVote.candidateName = CandidateName;
            newVote.voterAddress = msg.sender;
            voters[msg.sender].hasVoted = true;
            candidateMap[CandidateName].voteCount +=1; 

            hasValidVoterAddress = true;
        }

        return hasValidVoterAddress;
    }

    //FINISH STATE
    mapping(string => uint) private electionResultsMap;

    function setElectionResults() public
    isInThisState(VotingStates.Finish)
    {
        for(uint i =0; i< candidateNames.length;i++)
        {
            uint voteCount = candidateMap[candidateNames[i]].voteCount;
            electionResultsMap[candidateNames[i]] = voteCount;
        }
    }

    function nextStateFinishing() public
    adminOnly
    isInThisState(VotingStates.Voting)
    {
        votingState = VotingStates.Finish;
        setElectionResults();
    }

    function getResultsValue(string memory CandidateName) public
    isInThisState(VotingStates.Finish)
    view returns (uint )
    {
        return electionResultsMap[CandidateName];
    }


}