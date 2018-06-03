package com.sbk.callerid.service;

import com.sbk.callerid.model.CallerId;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.*;

@Service
public class CallerIdService implements ICallerIdService
{
    // Local store
    private Map<String, Map<String, String>> store = new TreeMap<>();

    /**
     * Note:
     * Sequence of Store Record     : number, context, name
     * Sequence of CallerId Class   : name, number, context
     */

    @Autowired
    private ResourceLoader resourceLoader;

    private static final String CSV_FILE_LOCATION = "data/interview-callerid-data.csv";

    @PostConstruct
    public void init()
    {
        System.out.println("Loading data from CSV file to CallerID Store...");
        int totalRecords = 0;
        Resource resource = resourceLoader.getResource("classpath:" + CSV_FILE_LOCATION);
        try
        {
            InputStream inputStream = resource.getInputStream();
            InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
            Iterable<CSVRecord> records = CSVFormat.DEFAULT.parse(inputStreamReader);

            for (CSVRecord record : records)
            {
                totalRecords++;
                String number = record.get(0);
                String context = record.get(1);
                String name = record.get(2);

                number = PhoneNumberHelper.convertPhoneNumber(number);

                //add only valid numbers to store
                if(!number.equals(PhoneNumberHelper.INVALID_INPUT))
                {
                    add(new CallerId(name, number, context));
                }
            }
        }
        catch (Exception e)
        {
            System.err.println("Can't load or parse CSV file: " + CSV_FILE_LOCATION);
        }
        System.out.println("Loaded total [ " + store.size() + " / " + totalRecords + " ] records.");
    }

    public boolean add(CallerId record)
    {
        if (null == store.get(record.getNumber()))
        {
            Map<String, String> newContext = new TreeMap<>();
            newContext.put(record.getContext(), record.getName());
            store.put(record.getNumber(), newContext);
        }
        else
        {
            Map<String, String> currentContext = store.get(record.getNumber());
            if (currentContext.get(record.getContext()) == null)
            {
                currentContext.put(record.getContext(), record.getName());
            }
            else
            {
                //context already exists for the phone number, throw error
                System.err.println("Context already exists for the phone number: " + record.toString());
                return false;
            }

        }
        return true;
    }

    public List<CallerId> get(String number)
    {
        List<CallerId> result = new ArrayList<>();

        if (null != store.get(number))
        {
            Map<String, String> currentContext = store.get(number);
            for (Map.Entry<String, String> entry : currentContext.entrySet())
            {
                CallerId record = new CallerId(entry.getValue(), number, entry.getKey());
                result.add(record);
            }
        }
        return result;
    }

    public boolean contains(String number)
    {
        return store.containsKey(number);
    }



}
