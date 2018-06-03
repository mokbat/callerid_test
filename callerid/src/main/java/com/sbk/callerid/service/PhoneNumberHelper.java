package com.sbk.callerid.service;

import com.google.i18n.phonenumbers.NumberParseException;
import com.google.i18n.phonenumbers.PhoneNumberUtil;
import com.google.i18n.phonenumbers.Phonenumber;

public class PhoneNumberHelper
{
    public static final String INVALID_INPUT = "-1";

    public static String convertPhoneNumber(String inputNumber)
    {
        if(inputNumber.isEmpty())
            return INVALID_INPUT;

        PhoneNumberUtil phoneUtil = PhoneNumberUtil.getInstance();
        Phonenumber.PhoneNumber number;
        try
        {
            number = phoneUtil.parse(inputNumber, "US");
        }
        catch (NumberParseException e)
        {
            System.err.println("NumberParseException was thrown: " + e.toString());
            return INVALID_INPUT;
        }

        return phoneUtil.format(number, PhoneNumberUtil.PhoneNumberFormat.E164);
    }
}
