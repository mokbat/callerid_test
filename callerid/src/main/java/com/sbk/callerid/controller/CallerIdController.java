package com.sbk.callerid.controller;

import com.sbk.callerid.service.ICallerIdService;
import com.sbk.callerid.service.PhoneNumberHelper;
import com.sbk.callerid.model.CallerId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@RestController
public class CallerIdController
{

    @Autowired
    public ICallerIdService idStore;

    @RequestMapping(value = "/query", method = RequestMethod.GET, produces = "application/json")
    @ResponseBody
    public ResponseEntity<?> queryCallerId(@RequestParam(value="number") String number)
    {
        String searchNumber = PhoneNumberHelper.convertPhoneNumber(number);
        if(searchNumber.equals(PhoneNumberHelper.INVALID_INPUT))
        {
            System.err.println("Search Number " + number + " is not a valid format.");
            String errorMsg = "{\"status\":400,\"error\":\"Bad Request\",\"message\":\"Invalid 'number' format\",\"path\":\"/query\"}";
            return new ResponseEntity<>(errorMsg, HttpStatus.BAD_REQUEST);
        }
        if(idStore.contains(searchNumber))
        {
            System.out.println("Search Number " + searchNumber + " is found.");
            Map<String, List<CallerId>> response = new LinkedHashMap<>();
            response.put("results", idStore.get(searchNumber));
            return new ResponseEntity<>(response, HttpStatus.OK);
        }
        else
        {
            System.err.println("Search Number " + searchNumber + " is not found.");
            String errorMsg = "{\"status\":404,\"error\":\"Not Found\",\"message\":\"Phone number in not found on the Server\",\"path\":\"/query\"}";
            return new ResponseEntity<>(errorMsg, HttpStatus.NOT_FOUND);
        }
    }

    @RequestMapping(value = "/number", method = RequestMethod.POST, produces = "application/json")
    public ResponseEntity<?> createCallerId(@RequestBody final @Valid CallerId newRecord)
    {
        //reformat phone number to E.164 format and check its validity
        newRecord.setNumber(PhoneNumberHelper.convertPhoneNumber(newRecord.getNumber()));
        if(newRecord.getNumber().equals(PhoneNumberHelper.INVALID_INPUT))
        {
            System.err.println("Search Number " + newRecord.getNumber() + " is not a valid format.");
            String errorMsg = "{\"status\":400,\"error\":\"Bad Request\",\"message\":\"Invalid 'number' format\",\"path\":\"/number\"}";
            return new ResponseEntity<>(errorMsg, HttpStatus.BAD_REQUEST);
        }

        //store the new record
        boolean saveStatus = idStore.add(newRecord);

        //send response
        if(saveStatus)
        {
            System.out.println("CallerID record " + newRecord + " saved.");
            return new ResponseEntity<>(newRecord, HttpStatus.CREATED);
        }
        else
        {
            System.err.println("CallerID record " + newRecord + " already exists.");
            String errorMsg = "{\"status\":406,\"error\":\"Not Acceptable\",\"message\":\"Phone number with the given context already exists.\",\"path\":\"/query\"}";
            return new ResponseEntity<>(errorMsg, HttpStatus.NOT_ACCEPTABLE);
        }
    }
}
